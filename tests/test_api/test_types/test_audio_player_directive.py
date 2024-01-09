import pytest

from aliceio.types import AudioPlayerItem, Stream
from aliceio.types.audio_player_directive import Action, AudioPlayerDirective


class TestAudioPlayerDirective:
    @pytest.mark.parametrize(
        "action",
        ["test", 42, None],
    )
    def test_wrong_action(self, action: str) -> None:
        with pytest.raises(ValueError):
            AudioPlayerDirective(
                action=action,
                item=AudioPlayerItem(
                    stream=Stream(
                        url="https://example.com/stream-audio-url",
                        offset_ms=0,
                        token="token",
                    )
                ),
            )

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
                )
            ),
        )
