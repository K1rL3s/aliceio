from typing import Optional

from .base import MutableAliceObject


class ShowItemMeta(MutableAliceObject):
    """https://yandex.ru/dev/dialogs/alice/doc/response-show-item-meta.html"""

    content_id: str
    publication_date: str
    title: Optional[str] = None
    title_tts: Optional[str] = None
    expiration_date: Optional[str] = None
