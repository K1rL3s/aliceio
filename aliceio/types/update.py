import contextlib
from typing import TYPE_CHECKING, Any, Optional, cast

from pydantic import model_validator

from ..enums import EventType, RequestType
from .account_linking_complete import AccountLinkingComplete
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

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request)
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
    account_linking_complete_event: Optional[AccountLinkingComplete] = None

    state: Optional[ApiState] = None

    if TYPE_CHECKING:
        event: AliceEvent
        event_type: str

        def __init__(
            __pydantic_self__,
            *,
            meta: Meta,
            request: AliceRequest,
            session: Session,
            version: str,
            message: Optional[Message] = None,
            audio_player: Optional[AudioPlayer] = None,
            button_pressed: Optional[ButtonPressed] = None,
            purchase: Optional[Purchase] = None,
            show_pull: Optional[ShowPull] = None,
            account_linking_complete_event: Optional[AccountLinkingComplete] = None,
            state: Optional[ApiState] = None,
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
                button_pressed=button_pressed,
                purchase=purchase,
                account_linking_complete_event=account_linking_complete_event,
                show_pull=show_pull,
                **__pydantic_kwargs,
            )

    else:

        @property
        def event(self) -> AliceEvent:
            return cast(AliceEvent, getattr(self, self.event_type))

        @property
        def event_type(self) -> str:
            if event_type := req_type_to_event_type.get(self.request.type):
                return str(event_type)
            raise UpdateTypeLookupError(
                "Update does not contain any known event type.",
            )

    # Это костыль для account_linking_complete_event, при нём нет поля request
    @model_validator(mode="before")
    @classmethod
    def _set_request_if_account_linking(cls, data: Any) -> Any:
        if isinstance(data, dict) and isinstance(
            data.get("account_linking_complete_event"),
            dict,
        ):
            data["request"] = {"type": RequestType.ACCOUNT_LINKING_COMPLETE}
        return data

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        with contextlib.suppress(UpdateTypeLookupError):
            # При работе ошибка возникнет ещё раз в диспетчере,
            # здесь она глушится для работы тестов.
            # TODO: убрать здесь suppress и переделать тесты
            self._event_model_validate(self.event_type, __context)

    def _event_model_validate(self, event_type: str, __context: Any) -> None:
        """
        Вспомогательный метод для определения и создания события конкретного типа.
        """
        dump = self.request.model_dump()
        dump["session"] = self.session
        event_model = event_type_to_event_model[event_type]
        setattr(
            self,
            event_type,
            event_model.model_validate(dump, context=__context),
        )


class UpdateTypeLookupError(LookupError):
    """Запрос не содержит ни одного известного типа событий."""


req_type_to_event_type: dict[str, str] = {
    RequestType.SIMPLE_UTTERANCE: EventType.MESSAGE,
    RequestType.BUTTON_PRESSED: EventType.BUTTON_PRESSED,
    RequestType.PURCHASE_CONFIRMATION: EventType.PURCHASE,
    RequestType.SHOW_PULL: EventType.SHOW_PULL,
    RequestType.AUDIO_PLAYER_STARTED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_FINISHED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_NEARLY_FINISHED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_STOPPED: EventType.AUDIO_PLAYER,
    RequestType.AUDIO_PLAYER_FAILED: EventType.AUDIO_PLAYER,
    RequestType.ACCOUNT_LINKING_COMPLETE: EventType.ACCOUNT_LINKING_COMPLETE,
}

event_type_to_event_model: dict[str, type[MutableAliceObject]] = {
    EventType.AUDIO_PLAYER: AudioPlayer,
    EventType.BUTTON_PRESSED: ButtonPressed,
    EventType.MESSAGE: Message,
    EventType.SHOW_PULL: ShowPull,
    EventType.PURCHASE: Purchase,
    EventType.UPDATE: Update,
    EventType.ACCOUNT_LINKING_COMPLETE: AccountLinkingComplete,
}
