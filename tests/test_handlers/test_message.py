from typing import Any

from aliceio.enums import RequestType
from aliceio.handlers import MessageHandler
from aliceio.types import Message
from tests.mocked import create_mocked_session


class TestMessageHandler:
    async def test_attributes_aliases(self):
        event = Message(
            type=RequestType.SIMPLE_UTTERANCE,
            command="test",
            original_utterance="test",
            session=create_mocked_session(),
            user=create_mocked_session().user,
        )

        class MyHandler(MessageHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user == self.event.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
