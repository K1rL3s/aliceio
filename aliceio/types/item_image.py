from typing import Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class ItemImage(MutableAliceObject):
    """
    Изображение в :class:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-desc
    """  # noqa

    image_id: Optional[str] = None  # Optional XD
    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[MediaButton] = None
