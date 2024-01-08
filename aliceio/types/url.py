from typing import Optional

from .base import AliceObject


class URL(AliceObject):
    """
    Ссылка на аудио или изображение в директиве аудио-плеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-art-desc

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-background-image-desc
    """  # noqa

    url: Optional[str] = None
