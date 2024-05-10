import contextlib
from typing import TYPE_CHECKING, Any, cast

from ..enums import EventType
from .alice_event import AliceEvent
from .base import MutableAliceObject
from .update import Update, UpdateTypeLookupError


# Если кто-то сможет лучше реализовать подмену update'а - буду благодарен
class TimeoutUpdate(Update):
    """Внутренннее событие, используется для реакции на выход за время ответа."""

    if TYPE_CHECKING:
        __init__ = Update.__init__

    else:

        @property
        def event(self) -> AliceEvent:
            return cast(AliceEvent, getattr(self, self._real_event_type))

        @property
        def event_type(self) -> str:
            return str(EventType.TIMEOUT)

    def model_post_init(self, __context: Any) -> None:
        MutableAliceObject.model_post_init(self, __context)
        with contextlib.suppress(UpdateTypeLookupError):
            self._event_model_validate(self._real_event_type, __context)

    @property
    def _real_event_type(self) -> str:
        return super().event_type
