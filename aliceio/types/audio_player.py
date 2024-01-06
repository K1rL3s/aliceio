from enum import Enum

from pydantic import field_validator

from aliceio.types import AliceObject, AudioPlayerItem


class AudioPlayer(AliceObject):
    """
    Директива аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html
    """

    action: str
    item: AudioPlayerItem

    @field_validator("action")
    @classmethod
    def action_validate(cls, v: str) -> str:
        if v not in Action:
            raise ValueError(
                f"AudioPlayer action must be "
                f'{", ".join(atype for atype in Action)}, not "{v}"'
            )
        return v


class Action(str, Enum):
    PLAY = "Play"
    STOP = "Stop"
