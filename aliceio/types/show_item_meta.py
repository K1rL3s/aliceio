from typing import Optional

from aliceio.types import AliceObject


class ShowItemMeta(AliceObject):
    """https://yandex.ru/dev/dialogs/alice/doc/response-show-item-meta.html"""

    content_id: str
    title: Optional[str] = None
    title_tts: Optional[str] = None
    publication_date: str
    expiration_date: Optional[str]
