from typing import Optional

from pydantic import UUID4

from .audio_player_error import AudioPlayerError
from .base import AliceObject
from .markup import Markup
from .nlu import NLU
from .payload import Payload


class AliceRequest(AliceObject):
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
