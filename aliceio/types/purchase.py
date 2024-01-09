from pydantic import UUID4

from .alice_event import AliceEvent
from .payload import Payload


class Purchase(AliceEvent):
    """
    Навык получает запрос с объектом request и типом Purchase.Confirmation,
    если пользователь выполняет оплату и навык должен отправить ему подтверждение.

    https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
    """

    type: str
    purchase_request_id: str
    purchase_token: UUID4
    order_id: str
    purchase_timestamp: int
    purchase_payload: Payload
    signed_data: str
    signature: str
