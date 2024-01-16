from typing import Any

from aliceio.enums import RequestType, ShowType
from aliceio.handlers import ShowPullHandler
from aliceio.types import ShowPull
from tests.mocked import create_mocked_session


class TestShowPullHandler:
    async def test_attributes_aliases(self):
        event = ShowPull(
            type=RequestType.SHOW_PULL,
            show_type=ShowType.MORNING,
            session=create_mocked_session(),
            user=create_mocked_session().user,
        )

        class MyHandler(ShowPullHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user == self.event.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
