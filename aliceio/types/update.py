from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Type, cast

from ..enums import EventType, RequestType
from .alice_event import AliceEvent
from .alice_request import AliceRequest
from .api_state import ApiState
from .audio_player import AudioPlayer
from .base import MutableAliceObject
from .button_pressed import ButtonPressed
from .message import Message
from .meta import Meta
from .purchase import Purchase
from .session import Session
from .show_pull import ShowPull


# Отнаследовать ли Update от AliceEvent'a?
class Update(MutableAliceObject):
    """
    Полный запрос от API Алисы.

    В любом запросе может присутствовать не более **одного** необязательного параметра.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/request.html)
    """

    meta: Meta
    request: AliceRequest
    session: Session
    version: str

    message: Optional[Message] = None
    audio_player: Optional[AudioPlayer] = None
    button_pressed: Optional[ButtonPressed] = None
    purchase: Optional[Purchase] = None
    show_pull: Optional[ShowPull] = None

    state: ApiState

    if TYPE_CHECKING:
        event: ClassVar[AliceEvent]
        event_type: ClassVar[str]

        def __init__(
            __pydantic_self__,
            *,
            meta: Meta,
            request: AliceRequest,
            session: Session,
            version: str,
            state: ApiState,
            message: Optional[Message] = None,
            audio_player: Optional[AudioPlayer] = None,
            button: Optional[ButtonPressed] = None,
            purchase: Optional[Purchase] = None,
            pull: Optional[ShowPull] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                meta=meta,
                request=request,
                session=session,
                version=version,
                state=state,
                message=message,
                audio_player=audio_player,
                button=button,
                purchase=purchase,
                pull=pull,
                **__pydantic_kwargs,
            )

    else:

        @property
        def event(self) -> AliceEvent:
            return cast(AliceEvent, getattr(self, self.event_type))

        @property
        def event_type(self) -> str:
            if (event_type := req_type_to_event_type.get(self.request.type)) is None:
                raise UpdateTypeLookupError(
                    "Update does not contain any known event type."
                )
            return str(event_type)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        try:
            self._event_model_validate(self.event_type, __context)
        except UpdateTypeLookupError:
            # При работе ошибка возникнет ещё раз в диспетчере,
            # здесь она глушится для работы тестов
            pass

    def _event_model_validate(self, event_type: str, __context: Any) -> None:
        """
        Вспомогательный метод для определения и создания события конкретного типа.
        """
        dump = self.request.model_dump()
        dump["session"] = self.session
        setattr(
            self,
            event_type,
            event_type_to_event_model[event_type].model_validate(
                dump, context=__context
            ),
        )


class UpdateTypeLookupError(LookupError):
    """Запрос не содержит ни одного известного типа событий."""


req_type_to_event_type: Dict[str, str] = {
    RequestType.SIMPLE_UTTERANCE: EventType.MESSAGE,
    RequestType.BUTTON_PRESSED: EventType.BUTTON_PRESSED,
    RequestType.PURCHASE_CONFIRMATION: EventType.PURCHASE,
    RequestType.SHOW_PULL: EventType.SHOW_PULL,
    RequestType.AUDIO_PLAYER_STARTED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_FINISHED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_NEARLY_FINISHED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_STOPPED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_FAILED: EventType.AUDIO_PLAYER,
}

event_type_to_event_model: Dict[str, Type[MutableAliceObject]] = {
    EventType.AUDIO_PLAYER: AudioPlayer,
    EventType.BUTTON_PRESSED: ButtonPressed,
    EventType.MESSAGE: Message,
    EventType.SHOW_PULL: ShowPull,
    EventType.PURCHASE: Purchase,
    EventType.UPDATE: Update,
}
