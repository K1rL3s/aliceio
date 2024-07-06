from typing import TYPE_CHECKING, Any, ClassVar

from .alice_event import AliceEvent
from .session import Session
from .update import Update


class ErrorEvent(AliceEvent):
    """Внутренннее событие, используется для получения ошибок при обработке событий."""

    update: Update
    exception: Exception

    if TYPE_CHECKING:
        event: ClassVar[AliceEvent]

        def __init__(
            __pydantic_self__,
            *,
            session: Session,  # из AliceEvent
            update: Update,
            exception: Exception,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                update=update,
                exception=exception,
                **__pydantic_kwargs,
            )

    else:

        @property
        def event(self) -> AliceEvent:
            return self.update.event
