from typing import TYPE_CHECKING, Any, Callable, Optional

from aliceio.dispatcher.event.bases import UNHANDLED, MiddlewareType, SkipHandler
from aliceio.dispatcher.event.handler import CallbackType, FilterObject, HandlerObject
from aliceio.dispatcher.middlewares.manager import MiddlewareManager
from aliceio.filters.base import Filter
from aliceio.types.base import AliceObject

if TYPE_CHECKING:
    from aliceio.dispatcher.router import Router


class AliceEventObserver:
    """
    Отслеживатель событий от Яндекс Диалогов.

    Здесь можно зарегистрировать обработчик с фильтром.
    Он остановит распространение события, когда пройдут фильтры любого обработчика.
    """

    def __init__(self, router: "Router", event_name: str) -> None:
        self.router = router
        self.event_name = event_name

        self.handlers: list[HandlerObject] = []

        self.middleware = MiddlewareManager()
        self.outer_middleware = MiddlewareManager()

        # Re-used filters check method from already implemented handler object
        # with dummy callback which never will be used
        self._handler = HandlerObject(callback=lambda: True, filters=[])

    def filter(self, *filters: CallbackType) -> None:
        """
        Добавление фильтров для всех обработчика этого наблюдателя.

        :param filters: Фильтры.
        """
        if self._handler.filters is None:
            self._handler.filters = []
        self._handler.filters.extend([FilterObject(filter_) for filter_ in filters])

    def _resolve_middlewares(self) -> list[MiddlewareType[AliceObject]]:
        middlewares: list[MiddlewareType[AliceObject]] = []
        for router in reversed(tuple(self.router.chain_head)):
            observer = router.observers.get(self.event_name)
            if observer:
                middlewares.extend(observer.middleware)

        return middlewares

    def register(
        self,
        callback: CallbackType,
        *filters: CallbackType,
        flags: Optional[dict[str, Any]] = None,
    ) -> CallbackType:
        """Добавление обработчика."""
        if flags is None:
            flags = {}

        for item in filters:
            if isinstance(item, Filter):
                item.update_handler_flags(flags=flags)

        self.handlers.append(
            HandlerObject(
                callback=callback,
                filters=[FilterObject(filter_) for filter_ in filters],
                flags=flags,
            ),
        )

        return callback

    def wrap_outer_middleware(
        self,
        callback: Any,
        event: AliceObject,
        data: dict[str, Any],
    ) -> Any:
        wrapped_outer = self.middleware.wrap_middlewares(
            self.outer_middleware,
            callback,
        )
        return wrapped_outer(event, data)

    def check_root_filters(self, event: AliceObject, **kwargs: Any) -> Any:
        return self._handler.check(event, **kwargs)

    async def trigger(self, event: AliceObject, **kwargs: Any) -> Any:
        """
        Распространения события на обработчики и остановка на первом совпадении.
        Обработчик будет вызван, когда все его фильтры будут пройдены.
        """
        for handler in self.handlers:
            kwargs["handler"] = handler
            result, data = await handler.check(event, **kwargs)
            if result:
                kwargs.update(data)
                try:
                    wrapped_inner = self.outer_middleware.wrap_middlewares(
                        self._resolve_middlewares(),
                        handler.call,
                    )
                    return await wrapped_inner(event, kwargs)
                except SkipHandler:
                    continue

        return UNHANDLED

    def __call__(
        self,
        *filters: CallbackType,
        flags: Optional[dict[str, Any]] = None,
    ) -> Callable[[CallbackType], CallbackType]:
        """Декоратор для регистрации обработчиков."""

        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(callback, *filters, flags=flags)
            return callback

        return wrapper
