from typing import Optional

from .base import MutableAliceObject
from .url import URL


class Metadata(MutableAliceObject):
    """
    Метадата аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-desc
    """  # noqa

    title: Optional[str] = None
    sub_title: Optional[str] = None
    art: Optional[URL] = None
    background_image: Optional[URL] = None
