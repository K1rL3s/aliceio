import pytest
from pydantic import ValidationError

from aliceio.exceptions import AliceWrongFieldError
from aliceio.types import AudioPlayerItem, Stream
from aliceio.types.audio_player_directive import Action, AudioPlayerDirective


class TestAudioPlayerDirective:
    @pytest.mark.parametrize(
        "action",
        ["test", 42, None],
    )
    def test_wrong_action(self, action) -> None:
        item = AudioPlayerItem(
            stream=Stream(
                url="https://example.com/stream-audio-url",
                offset_ms=0,
                token="token",
            ),
        )
        if isinstance(action, str):
            with pytest.raises(AliceWrongFieldError):
                AudioPlayerDirective(action=action, item=item)
        else:
            with pytest.raises(ValidationError):
                AudioPlayerDirective(action=action, item=item)

    @pytest.mark.parametrize(
        "action",
        [Action.PLAY, Action.STOP, "play", "stop", "STOP", "PLAY"],
    )
    def test_good_action(self, action: str) -> None:
        AudioPlayerDirective(
            action=action,
            item=AudioPlayerItem(
                stream=Stream(
                    url="https://example.com/stream-audio-url",
                    offset_ms=0,
                    token="token",
                ),
            ),
        )
