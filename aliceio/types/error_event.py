from typing import TYPE_CHECKING, Any

from .alice_event import AliceEvent
from .session import Session
from .update import Update


class ErrorEvent(AliceEvent):
    """Внутренннее событие, используется для получения ошибок при обработке событий."""

    update: Update
    exception: Exception

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            update: Update,
            exception: Exception,
            session: Session,  # из AliceEvent
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                update=update,
                exception=exception,
                session=session,
                **__pydantic_kwargs,
            )

    @property
    def event(self) -> AliceEvent:
        return self.update.event
