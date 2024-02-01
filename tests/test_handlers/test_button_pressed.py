from typing import Any

from aliceio.enums import RequestType
from aliceio.handlers import ButtonPressedHandler
from aliceio.types import ButtonPressed
from tests.mocked import create_mocked_session


class TestButtonPressedHandler:
    async def test_attributes_aliases(self):
        event = ButtonPressed(
            type=RequestType.BUTTON_PRESSED,
            payload={"k": "v"},
            session=create_mocked_session(),
        )

        class MyHandler(ButtonPressedHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user == self.event.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
