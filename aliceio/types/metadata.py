from typing import Optional

from aliceio.types import AliceObject, URL


class Metadata(AliceObject):
    """
    Метадата аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-desc
    """  # noqa

    title: Optional[str] = None
    sub_title: Optional[str] = None
    art: Optional[URL] = None
    background_image: Optional[URL] = None
