from typing import Optional

from aliceio.types import AliceObject, MediaButton


class ImageGalleryItem(AliceObject):
    """
    Изображение в :class:`ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-desc
    """  # noqa

    image_id: str
    title: Optional[str]
    button: Optional[MediaButton] = None
