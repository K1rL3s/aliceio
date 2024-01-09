from typing import Any, Dict, Optional, Type, cast

from ..enums import EventType, RequestType
from .alice_event import AliceEvent
from .alice_request import AliceRequest
from .audio_player import AudioPlayer
from .base import MutableAliceObject
from .button import Button
from .message import Message
from .meta import Meta
from .pull import Pull
from .purchase import Purchase
from .session import Session


class Update(MutableAliceObject):
    """
    Полный запрос от API Алисы.

    В любом запросе может присутствовать не более **одного** необязательного параметра.

    https://yandex.ru/dev/dialogs/alice/doc/request.html
    """

    meta: Meta
    request: AliceRequest
    session: Session
    version: str

    message: Optional[Message] = None
    audio_player: Optional[AudioPlayer] = None
    button: Optional[Button] = None
    purchase: Optional[Purchase] = None
    pull: Optional[Pull] = None

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        events: Dict[str, Type[MutableAliceObject]] = {
            EventType.AUDIO_PLAYER: AudioPlayer,
            EventType.BUTTON: Button,
            EventType.MESSAGE: Message,
            EventType.PULL: Pull,
            EventType.PURCHASE: Pull,
            EventType.UPDATE: Update,
        }

        data = self.request.model_dump()
        data.update({"session": self.session, "user": self.session.user})
        try:
            setattr(
                self,
                self.event_type,
                events[self.event_type].model_validate(data, context=__context),
            )
        except UpdateTypeLookupError:
            # При работе ошибка возникнет ещё раз в диспетчере,
            # здесь она глушится для работы тестов
            pass

    @property
    def event(self) -> AliceEvent:
        return cast(AliceEvent, getattr(self, self.event_type))

    @property
    def event_type(self) -> str:
        event_types: Dict[str, str] = {
            RequestType.SIMPLE_UTTERANCE: EventType.MESSAGE,
            RequestType.BUTTON_PRESSED: EventType.BUTTON,
            RequestType.PURCHASE_CONFIRMATION: EventType.PURCHASE,
            RequestType.SHOW_PULL: EventType.PULL,
            RequestType.AUDIO_PLAYER_STARTED: EventType.AUDIO_PLAYER,
            RequestType.AUDIO_PLAYER_FINISHED: EventType.AUDIO_PLAYER,
            RequestType.AUDIO_PLAYER_NEARLY_FINISHED: EventType.AUDIO_PLAYER,
            RequestType.AUDIO_PLAYER_STOPPED: EventType.AUDIO_PLAYER,
            RequestType.AUDIO_PLAYER_FAILED: EventType.AUDIO_PLAYER,
        }
        if (event_type := event_types.get(self.request.type)) is None:
            raise UpdateTypeLookupError("Update does not contain any known event type.")
        return str(event_type)


class UpdateTypeLookupError(LookupError):
    """Запрос не содержит ни одного известного типа событий."""
