from typing import Any

from aliceio.handlers import TimeoutHandler
from aliceio.types import TimeoutUpdate, Update


class TestTimeoutHandler:
    async def test_attributes_aliases(self, update: Update):
        event = TimeoutUpdate.model_validate(update.model_dump())

        class MyHandler(TimeoutHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.session.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
