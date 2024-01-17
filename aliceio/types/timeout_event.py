from typing import TYPE_CHECKING, Any

from .alice_event import AliceEvent
from .update import Update


class TimeoutEvent(AliceEvent):
    """Внутренннее событие, используется для реакции на выход за время ответа."""

    update: Update

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            update: Update,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                update=update,
                **__pydantic_kwargs,
            )

    @property
    def event(self) -> AliceEvent:
        return self.update.event
