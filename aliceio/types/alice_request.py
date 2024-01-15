from typing import TYPE_CHECKING, Any, Optional

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
    payload: Optional[Payload] = None
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
    purchase_token: Optional[str] = None
    order_id: Optional[str] = None
    purchase_timestamp: Optional[int] = None
    purchase_payload: Optional[Payload] = None
    signed_data: Optional[str] = None
    signature: Optional[str] = None

    # not null при запуске утреннего шоу Алисы
    # https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    show_type: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            payload: Optional[Payload] = None,
            command: Optional[str] = None,
            original_utterance: Optional[str] = None,
            markup: Optional[Markup] = None,
            nlu: Optional[NLU] = None,
            error: Optional[AudioPlayerError] = None,
            purchase_request_id: Optional[str] = None,
            purchase_token: Optional[str] = None,
            order_id: Optional[str] = None,
            purchase_timestamp: Optional[int] = None,
            purchase_payload: Optional[Payload] = None,
            signed_data: Optional[str] = None,
            signature: Optional[str] = None,
            show_type: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                payload=payload,
                command=command,
                original_utterance=original_utterance,
                markup=markup,
                nlu=nlu,
                error=error,
                purchase_request_id=purchase_request_id,
                purchase_token=purchase_token,
                order_id=order_id,
                purchase_timestamp=purchase_timestamp,
                purchase_payload=purchase_payload,
                signed_data=signed_data,
                signature=signature,
                show_type=show_type,
                **__pydantic_kwargs,
            )
