from typing import Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class ItemImage(MutableAliceObject):
    """
    Изображение в :class:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-desc
    """  # noqa

    image_id: str
    title: str
    description: str
    button: Optional[MediaButton] = None
