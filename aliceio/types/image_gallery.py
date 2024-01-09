from typing import List

from pydantic import field_validator

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

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.IMAGE_GALLERY.lower():
            raise ValueError(
                f'ImageGallery type must be "{CardType.IMAGE_GALLERY}", not "{v}"'
            )
        return CardType.IMAGE_GALLERY
