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

    async def test_is_ping(self):
        event = Message(
            type=RequestType.SIMPLE_UTTERANCE,
            command="",
            original_utterance="ping",
            session=create_mocked_session(),
        )

        assert event.is_ping

        event = Message(
            type=RequestType.SIMPLE_UTTERANCE,
            command="",
            original_utterance="not ping",
            session=create_mocked_session(),
        )

        assert not event.is_ping
