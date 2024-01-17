from typing import Any

from aliceio.enums import RequestType
from aliceio.handlers import AudioPlayerHandler
from aliceio.types import AudioPlayer, AudioPlayerError
from tests.mocked import create_mocked_session


class TestAudioPlayerHandler:
    async def test_attributes_aliases(self):
        event = AudioPlayer(
            type=RequestType.AUDIO_PLAYER_FAILED,
            error=AudioPlayerError(
                message="Something wrong", type="MEDIA_ERROR_UNKNOWN"
            ),
            session=create_mocked_session(),
        )

        class MyHandler(AudioPlayerHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user == self.event.user
                assert self.session == self.event.session
                return True

        assert await MyHandler(event)
