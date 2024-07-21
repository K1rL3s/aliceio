from typing import TYPE_CHECKING, Any

from .alice_event import AliceEvent
from .payload import Payload
from .session import Session


class Purchase(AliceEvent):
    """
    Навык получает запрос с объектом request и типом Purchase.Confirmation,
    если пользователь выполняет оплату и навык должен отправить ему подтверждение.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request-purchase-confirmation)
    """

    type: str
    purchase_request_id: str
    purchase_token: str
    order_id: str
    purchase_timestamp: int
    purchase_payload: Payload
    signed_data: str
    signature: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            session: Session,  # из AliceEvent
            type: str,
            purchase_request_id: str,
            purchase_token: str,
            order_id: str,
            purchase_timestamp: int,
            purchase_payload: Payload,
            signed_data: str,
            signature: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                type=type,
                purchase_request_id=purchase_request_id,
                purchase_token=purchase_token,
                order_id=order_id,
                purchase_timestamp=purchase_timestamp,
                purchase_payload=purchase_payload,
                signed_data=signed_data,
                signature=signature,
                **__pydantic_kwargs,
            )
