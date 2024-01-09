from typing import List

from ..enums.card import CardType
from .card import Card
from .image_gallery_item import ImageGalleryItem


class ImageGallery(Card):
    """
    :class:`Card` с типом :code:`ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html
    """

    type: str = CardType.IMAGE_GALLERY

    items: List[ImageGalleryItem]
