from enum import Enum
from typing import cast, Optional

from pydantic import field_validator, UUID4

from aliceio.types import AliceObject, AudioPlayerError, Markup, NLU
from aliceio.types.payload import Payload


class Request(AliceObject):
    """
    Запрос с информацией от пользователя от API Алисы.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__request-desc
    """

    type: str
    payload: Payload
    command: Optional[str] = None
    original_utterance: Optional[str] = None
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None

    # Ошибка в аудиоплеере
    # https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    error: Optional[AudioPlayerError] = None

    # not null при type == RequestType.PURCHASE_CONFIRMATION
    # https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
    purchase_request_id: Optional[str] = None
    purchase_token: Optional[UUID4] = None
    order_id: Optional[str] = None
    purchase_timestamp: Optional[int] = None
    purchase_payload: Optional[Payload] = None
    signed_data: Optional[str] = None
    signature: Optional[str] = None

    # not null при запуске утреннего шоу Алисы
    # https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    show_type: Optional[str] = None

    @field_validator("type")
    @classmethod
    def request_type_validator(cls, v: str) -> str:
        if v not in RequestType:
            raise ValueError(
                f'Request "type" must be '
                f'{", ".join(rtype for rtype in RequestType)}, not "{v}"'
            )
        return v

    @field_validator("show_type")
    @classmethod
    def show_type_validator(cls, v: Optional[str]) -> str:
        if v and v not in ShowType:
            raise ValueError(
                f'Request "show_type" must be '
                f'{", ".join(stype for stype in ShowType)}, not "{v}"'
            )
        return v

    def __post_init__(self):
        if self.markup is not None:
            self.markup = Markup(**cast(dict, self.markup))


class RequestType(str, Enum):
    AUDIO_PLAYER_STARTED = "AudioPlayer.PlaybackStarted"
    AUDIO_PLAYER_FINISHED = "AudioPlayer.PlaybackFinished"
    AUDIO_PLAYER_NEARLY_FINISHED = "AudioPlayer.PlaybackNearlyFinished"
    AUDIO_PLAYER_STOPPED = "AudioPlayer.PlaybackStopped"
    AUDIO_PLAYER_FAILED = "AudioPlayer.PlaybackFailed"
    BUTTON_PRESSED = "ButtonPressed"
    PURCHASE_CONFIRMATION = "Purchase.Confirmation"
    SHOW_PULL = "Show.Pull"
    SIMPLE_UTTERANCE = "SimpleUtterance"


class ShowType(str, Enum):
    MORNING = "MORNING"
