from __future__ import annotations

from collections.abc import Generator
from typing import Any, Final, Optional

from ..enums import EventType
from ..types.base import AliceObject
from .event.alice import AliceEventObserver
from .event.bases import REJECTED, UNHANDLED
from .event.event import EventObserver

INTERNAL_UPDATE_TYPES: Final[frozenset[str]] = frozenset({"update", "error", "timeout"})


class Router:
    """
    Обработчики могут быть добавлены в наблюдатель двумя способами:

    - Через метод:
        `router.<event_type>.register(handler, <filters, ...>)`
    - Через декоратор:
        `@router.<event_type>(<filters, ...>)`
    """

    def __init__(self, *, name: Optional[str] = None) -> None:
        """
        :param name: Имя роутера, может быть полезно для отладки.
        """

        self.name = name or hex(id(self))

        self._parent_router: Optional[Router] = None
        self._sub_routers: list[Router] = []

        # Наблюдатели
        self.message = AliceEventObserver(router=self, event_name=EventType.MESSAGE)
        self.purchase = AliceEventObserver(router=self, event_name=EventType.PURCHASE)
        self.show_pull = AliceEventObserver(router=self, event_name=EventType.SHOW_PULL)
        self.button_pressed = AliceEventObserver(
            router=self,
            event_name=EventType.BUTTON_PRESSED,
        )
        self.audio_player = AliceEventObserver(
            router=self,
            event_name=EventType.AUDIO_PLAYER,
        )
        self.account_linking_complete = AliceEventObserver(
            router=self,
            event_name=EventType.ACCOUNT_LINKING_COMPLETE,
        )
        self.errors = self.error = AliceEventObserver(
            router=self,
            event_name=EventType.ERROR,
        )
        self.timeout = AliceEventObserver(router=self, event_name=EventType.TIMEOUT)

        self.startup = EventObserver()
        self.shutdown = EventObserver()

        self.observers: dict[str, AliceEventObserver] = {
            EventType.MESSAGE: self.message,
            EventType.BUTTON_PRESSED: self.button_pressed,
            EventType.PURCHASE: self.purchase,
            EventType.SHOW_PULL: self.show_pull,
            EventType.AUDIO_PLAYER: self.audio_player,
            EventType.ACCOUNT_LINKING_COMPLETE: self.account_linking_complete,
            EventType.ERROR: self.errors,
            EventType.TIMEOUT: self.timeout,
        }

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name!r}"

    def __repr__(self) -> str:
        return f"<{self}>"

    async def propagate_event(
        self,
        event_type: str,
        event: AliceObject,
        **kwargs: Any,
    ) -> Any:
        kwargs.update(event_router=self)
        observer = self.observers.get(event_type)

        async def _wrapped(alice_event: AliceObject, **data: Any) -> Any:
            return await self._propagate_event(
                observer=observer,
                event_type=event_type,
                event=alice_event,
                **data,
            )

        if observer:
            return await observer.wrap_outer_middleware(
                _wrapped,
                event=event,
                data=kwargs,
            )
        return await _wrapped(event, **kwargs)

    async def _propagate_event(
        self,
        observer: Optional[AliceEventObserver],
        event_type: str,
        event: AliceObject,
        **kwargs: Any,
    ) -> Any:
        response = UNHANDLED
        if observer:
            # Прежде чем проверять какой-либо обработчик,
            # надо проверить глобально определенные фильтры на роутере.
            # Эта проверка помещена здесь вместо метода триггера,
            # чтобы добавить возможность для передачи контекста
            # обработчикам из этих фильтров.
            result, data = await observer.check_root_filters(event, **kwargs)
            if not result:
                return UNHANDLED
            kwargs.update(data)

            response = await observer.trigger(event, **kwargs)
            if response is REJECTED:  # pragma: no cover
                # Возможно, только если какой-то обработчик возвращает REJECTED
                return UNHANDLED
            if response is not UNHANDLED:
                return response

        for router in self._sub_routers:
            response = await router.propagate_event(
                event_type=event_type,
                event=event,
                **kwargs,
            )
            if response is not UNHANDLED:
                break

        return response

    @property
    def chain_head(self) -> Generator[Router, None, None]:
        router: Optional[Router] = self
        while router:
            yield router
            router = router.parent_router

    @property
    def chain_tail(self) -> Generator[Router, None, None]:
        yield self
        for router in self._sub_routers:
            yield from router.chain_tail

    @property
    def parent_router(self) -> Optional[Router]:
        return self._parent_router

    @parent_router.setter
    def parent_router(self, router: Router) -> None:
        """
        Установщик родительского роутера этого экземпляра роутера.
        Не используйте этот метод в вашем коде.
        Все роутеры должны подключаться через метод :code:`include_router`

        Запрещены само- и циклические ссылки в роутерах.

        :param router: Роутер.
        """
        if not isinstance(router, Router):
            raise TypeError(
                f"router should be instance of Router not {type(router).__name__!r}",
            )
        if self._parent_router:
            raise RuntimeError(f"Router is already attached to {self._parent_router!r}")
        if self == router:
            raise RuntimeError("Self-referencing routers is not allowed")

        parent: Optional[Router] = router
        while parent is not None:
            if parent == self:
                raise RuntimeError("Circular referencing of Router is not allowed")

            parent = parent.parent_router

        self._parent_router = router
        router._sub_routers.append(self)  # noqa: SLF001

    def include_routers(self, *routers: Router) -> None:
        """
        Подключение нескольких роутеров.

        :param routers: Роутеры.
        """
        if not routers:
            raise ValueError("At least one router must be provided")
        for router in routers:
            self.include_router(router)

    def include_router(self, router: Router) -> Router:
        """
        Подключение другого роутера.

        :param router: Роутер.
        :return: Этот же роутер.
        """
        if not isinstance(router, Router):
            raise TypeError(
                f"router should be instance of Router, "
                f"not {type(router).__class__.__name__}",
            )
        router.parent_router = self
        return router

    async def emit_startup(self, *args: Any, **kwargs: Any) -> None:
        """Рекурсивный вызов callback'ов при запуске."""
        kwargs.update(router=self)
        await self.startup.trigger(*args, **kwargs)
        for router in self._sub_routers:
            await router.emit_startup(*args, **kwargs)

    async def emit_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """
        Рекурсивный вызывов callback'ов выключения для корректного завершения работы.
        """
        kwargs.update(router=self)
        await self.shutdown.trigger(*args, **kwargs)
        for router in self._sub_routers:
            await router.emit_shutdown(*args, **kwargs)
