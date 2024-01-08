from typing import Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class ImageGalleryItem(MutableAliceObject):
    """
    Изображение в :class:`ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-desc
    """  # noqa

    image_id: str
    title: Optional[str] = None
    button: Optional[MediaButton] = None
