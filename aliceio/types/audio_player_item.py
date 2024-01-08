from typing import Optional

from .base import MutableAliceObject
from .metadata import Metadata
from .stream import Stream


class AudioPlayerItem(MutableAliceObject):
    """
    Данные директивы аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-desc
    """  # noqa

    stream: Stream
    metadata: Optional[Metadata] = None
