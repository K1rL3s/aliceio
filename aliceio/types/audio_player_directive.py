from pydantic import field_validator

from ..enums.base import StrEnum, ValuesEnum
from .audio_player_item import AudioPlayerItem
from .base import MutableAliceObject


class AudioPlayerDirective(MutableAliceObject):
    """
    Директива аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html
    """

    action: str
    item: AudioPlayerItem

    @field_validator("action")
    @classmethod
    def action_validate(cls, v: str) -> str:
        if v.capitalize() not in Action.values():
            raise ValueError(
                f"AudioPlayer action must be "
                f'{", ".join(atype for atype in Action)}, not "{v}"'
            )
        return v.capitalize()


class Action(StrEnum, ValuesEnum):
    PLAY = "Play"
    STOP = "Stop"
