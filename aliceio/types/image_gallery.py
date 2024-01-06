from typing import List

from aliceio.types import Card, CardType, ImageGalleryItem


class ImageGallery(Card):
    """
    Card с типом `ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html
    """

    type: str = CardType.IMAGE_GALLERY

    items: List[ImageGalleryItem]
