from aliceio.enums import RequestType
from aliceio.types import Message
from tests.mocked import create_mocked_session


class TestMessage:
    async def test_attributes_aliases(self):
        event = Message(
            type=RequestType.SIMPLE_UTTERANCE,
            command="test",
            original_utterance="test_real",
            session=create_mocked_session(),
        )

        assert event.original_utterance == event.original_text == event.original_command
        assert event.command == event.text
