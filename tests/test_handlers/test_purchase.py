from typing import Any

from aliceio.enums import RequestType
from aliceio.handlers import PurchaseHandler
from aliceio.types import Purchase
from tests.mocked import create_mocked_session


class TestPurchaseHandler:
    async def test_attributes_aliases(self):
        event = Purchase(
            type=RequestType.PURCHASE_CONFIRMATION,
            purchase_request_id="id",
            purchase_token="token",
            order_id="order_id",
            purchase_timestamp=1,
            purchase_payload={"k": "v"},
            signed_data="data",
            signature="sign",
            session=create_mocked_session(),
        )

        class MyHandler(PurchaseHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user == self.event.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
