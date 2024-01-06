from typing import Optional

from aliceio.types import AliceObject, Metadata, Stream


class AudioPlayerItem(AliceObject):
    """
    Данные директивы аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-desc
    """  # noqa

    stream: Stream
    metadata: Optional[Metadata] = None
