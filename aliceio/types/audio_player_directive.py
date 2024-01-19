from typing import TYPE_CHECKING, Any

from pydantic import field_validator

from ..enums.base import StrEnum, ValuesEnum
from ..exceptions import AliceWrongFieldError
from .audio_player_item import AudioPlayerItem
from .base import MutableAliceObject


class AudioPlayerDirective(MutableAliceObject):
    """
    Директива аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html
    """

    action: str
    item: AudioPlayerItem

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            action: str,
            item: AudioPlayerItem,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                action=action,
                item=item,
                **__pydantic_kwargs,
            )

    @field_validator("action")
    @classmethod
    def action_validate(cls, v: str) -> str:
        if v.capitalize() not in Action.values():
            raise AliceWrongFieldError(
                f"AudioPlayer action must be "
                f'{", ".join(atype for atype in Action)}, not "{v}"'
            )
        return v.capitalize()


class Action(StrEnum, ValuesEnum):
    PLAY = "Play"
    STOP = "Stop"
