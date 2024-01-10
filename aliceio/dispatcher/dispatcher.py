from __future__ import annotations

import asyncio
import contextvars
import warnings
from asyncio import CancelledError, Event, Future, Lock
from typing import Any, Dict, Optional, Set, Union

from .. import loggers
from ..client.skill import Skill
from ..enums import EventType
from ..exceptions import AliceAPIError
from ..fsm.middleware import FSMContextMiddleware
from ..fsm.storage.base import BaseStorage
from ..fsm.storage.memory import MemoryStorage
from ..fsm.strategy import FSMStrategy
from ..methods import AliceMethod, AliceType
from ..types import Update, UpdateTypeLookupError
# from ..utils.backoff import BackoffConfig
from .event.alice import AliceEventObserver
from .event.bases import UNHANDLED, SkipHandler
from .middlewares.error import ErrorsMiddleware
from .middlewares.user_context import UserContextMiddleware
from .router import Router

# DEFAULT_BACKOFF_CONFIG = BackoffConfig(
#     min_delay=1.0, max_delay=5.0, factor=1.3, jitter=0.1
# )


# TODO: Сделать загрузку, запрос и удаление изображений и аудио
class Dispatcher(Router):
    """Главный роутер."""

    def __init__(
        self,
        *,
        storage: Optional[BaseStorage] = None,
        fsm_strategy: FSMStrategy = FSMStrategy.USER,
        disable_fsm: bool = False,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Главный роутер

        :param storage: Хранилище для FSM
        :param fsm_strategy: Стратегия FSM
        :param disable_fsm: Отключить ли FSM
        :param kwargs: Остальные аргументы,
                       будут переданы в обработчики как именованные аргументы
        """
        super(Dispatcher, self).__init__(name=name)

        self.update = self.observers["update"] = AliceEventObserver(
            router=self,
            event_name=EventType.UPDATE,
        )
        self.update.register(self._listen_update)

        # Error handlers should work is out of all other functions
        # and should be registered before all others middlewares
        self.update.outer_middleware(ErrorsMiddleware(self))

        # User context middleware makes small optimization for all other builtin
        # middlewares via caching the user and chat instances in the event context
        self.update.outer_middleware(UserContextMiddleware())

        # FSM middleware should always be registered after User context middleware
        # because here is used context from previous step
        self.fsm = FSMContextMiddleware(
            storage=storage or MemoryStorage(),
            strategy=fsm_strategy,
        )
        if not disable_fsm:
            self.update.outer_middleware(self.fsm)
        self.shutdown.register(self.fsm.close)

        self.workflow_data: Dict[str, Any] = kwargs
        self._running_lock = Lock()
        self._stop_signal: Optional[Event] = None
        self._stopped_signal: Optional[Event] = None
        self._handle_update_tasks: Set[asyncio.Task[Any]] = set()

    def __getitem__(self, item: str) -> Any:
        return self.workflow_data[item]

    def __setitem__(self, key: str, value: Any) -> None:
        self.workflow_data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.workflow_data[key]

    def get(self, key: str, /, default: Optional[Any] = None) -> Optional[Any]:
        return self.workflow_data.get(key, default)

    @property
    def storage(self) -> BaseStorage:
        return self.fsm.storage

    @property
    def parent_router(self) -> Optional[Router]:
        """
        У диспетчера нет родительского маршрутизатора
        и он не может быть включен ни в какие другие роутеры или диспетчеры.
        """
        return None  # noqa: RET501

    @parent_router.setter
    def parent_router(self, value: Router) -> None:
        """
        Диспетчер является корневым маршрутизатором,
        поэтому ему нельзя настроить родительский роутер.
        """
        raise RuntimeError("Dispatcher can not be attached to another Router.")

    async def feed_update(self, skill: Skill, update: Update, **kwargs: Any) -> Any:
        """
        Main entry point for incoming updates
        Response of this method can be used as Webhook response

        :param skill:
        :param update:
        """
        loop = asyncio.get_running_loop()
        handled = False
        start_time = loop.time()

        if update.skill != skill:
            # Re-mounting update to the current skill instance for making possible to
            # use it in shortcuts.
            # Here is update is re-created because we need to propagate context to
            # all nested objects and attributes of the Update, but it
            # is impossible without roundtrip to JSON :(
            # The preferred way is that pass already mounted Skill instance to this update
            # before call feed_update method
            update = Update.model_validate(
                update.model_dump(), context={"skill": skill}
            )

        try:
            response = await self.update.wrap_outer_middleware(
                self.update.trigger,
                update,
                {
                    **self.workflow_data,
                    **kwargs,
                    "skill": skill,
                },
            )
            handled = response is not UNHANDLED
            return response
        finally:
            finish_time = loop.time()
            duration = (finish_time - start_time) * 1000
            loggers.event.info(
                "Update from session=%s is %s. Duration %d ms by skill id=%d",
                update.session.session_id,
                "handled" if handled else "not handled",
                duration,
                skill.id,
            )

    async def feed_raw_update(
        self,
        skill: Skill,
        update: Dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        """
        Main entry point for incoming updates with automatic Dict->Update serializer

        :param skill:
        :param update:
        :param kwargs:
        """
        parsed_update = Update.model_validate(update, context={"skill": skill})
        return await self.feed_update(skill=skill, update=parsed_update, **kwargs)

    @classmethod
    async def silent_call_request(
        cls,
        skill: Skill,
        result: AliceMethod[Any],
    ) -> None:
        """
        Simulate answer into WebHook

        :param skill:
        :param result:
        :return:
        """
        try:
            await skill(result)
        except AliceAPIError as e:
            # In due to WebHook mechanism doesn't allow getting response for
            # requests called in answer to WebHook request.
            # Need to skip unsuccessful responses.
            # For debugging here is added logging.
            loggers.event.error(
                "Failed to make answer: %s: %s", e.__class__.__name__, e
            )

    async def _listen_update(self, update: Update, **kwargs: Any) -> Any:
        """
        Main updates listener

        Workflow:
        - Detect content type and propagate to observers in current router
        - If no one filter is pass - propagate update to child routers as Update

        :param update:
        :param kwargs:
        :return:
        """
        try:
            event_type = update.event_type
            event = update.event
        except UpdateTypeLookupError as e:
            warnings.warn(
                "Detected unknown update type.\n"
                "Seems like Alice API was updated and you have "
                "installed not latest version of aliceio framework"
                f"\nUpdate: {update.model_dump_json(exclude_unset=True)}",
                RuntimeWarning,
            )
            raise SkipHandler() from e

        kwargs.update(event_update=update)

        return await self.propagate_event(
            event_type=event_type,
            event=event,
            **kwargs,
        )

    async def _process_update(
        self,
        skill: Skill,
        update: Update,
        call_answer: bool = True,
        **kwargs: Any,
    ) -> bool:
        """
        Propagate update to event listeners

        :param skill: instance of Skill
        :param update: instance of Update
        :param call_answer: need to execute response as Alice method
                            (like answer into webhook)
        :param kwargs: contextual data for middlewares, filters and handlers
        :return: status
        """
        try:
            response = await self.feed_update(skill, update, **kwargs)
            if call_answer and isinstance(response, AliceMethod):
                await self.silent_call_request(skill=skill, result=response)
            return response is not UNHANDLED

        except Exception as e:
            loggers.event.exception(
                "Cause exception while process update "
                "session=%s by skill id=%d\n%s: %s",
                update.session.session_id,
                skill.id,
                e.__class__.__name__,
                e,
            )
            return True  # because update was processed but unsuccessful

    async def _feed_webhook_update(
        self, skill: Skill, update: Update, **kwargs: Any
    ) -> Any:
        """
        The same with `Dispatcher.process_update()`
        but returns real response instead of bool
        """
        try:
            return await self.feed_update(skill, update, **kwargs)
        except Exception as e:
            loggers.event.exception(
                "Cause exception while process update "
                "session=%s by skill id=%d\n%s: %s",
                update.session.session_id,
                skill.id,
                e.__class__.__name__,
                e,
            )
            raise

    # TODO: Сделать под Алису
    async def feed_webhook_update(
        self,
        skill: Skill,
        update: Union[Update, Dict[str, Any]],
        _timeout: float = 55,
        **kwargs: Any,
    ) -> Optional[AliceMethod[AliceType]]:
        if not isinstance(update, Update):  # Allow to use raw updates
            update = Update.model_validate(update, context={"skill": skill})

        ctx = contextvars.copy_context()
        loop = asyncio.get_running_loop()
        waiter = loop.create_future()

        def release_waiter(*_: Any) -> None:
            if not waiter.done():
                waiter.set_result(None)

        timeout_handle = loop.call_later(_timeout, release_waiter)

        process_updates: Future[Any] = asyncio.ensure_future(
            self._feed_webhook_update(skill=skill, update=update, **kwargs)
        )
        process_updates.add_done_callback(release_waiter, context=ctx)

        def process_response(task: Future[Any]) -> None:
            warnings.warn(
                "Detected slow response into webhook.\n"
                "Alice is waiting for response only 4.5 seconds and cancel update.\n"
                "For preventing this situation response into webhook returned immediately "
                "and handler is moved to background and still processing update.",
                RuntimeWarning,
            )
            try:
                result = task.result()
            except Exception as e:
                raise e
            if isinstance(result, AliceMethod):
                asyncio.ensure_future(
                    self.silent_call_request(skill=skill, result=result)
                )

        try:
            try:
                await waiter
            except CancelledError:  # pragma: no cover
                process_updates.remove_done_callback(release_waiter)
                process_updates.cancel()
                raise

            if process_updates.done():
                # TODO: handle exceptions
                response: Any = process_updates.result()
                if isinstance(response, AliceMethod):
                    return response

            else:
                process_updates.remove_done_callback(release_waiter)
                process_updates.add_done_callback(process_response, context=ctx)

        finally:
            timeout_handle.cancel()

        return None
