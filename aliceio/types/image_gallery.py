from typing import List, Optional

from pydantic import Field, field_validator

from ..enums import CardType
from .base import MutableAliceObject
from .image_gallery_item import ImageGalleryItem


class ImageGallery(MutableAliceObject):
    """
    :code:`Card` с типом :code:`ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html
    """

    type: str = CardType.IMAGE_GALLERY

    items: Optional[List[ImageGalleryItem]] = Field(
        default_factory=list,
        min_length=1,
        max_length=10,
    )

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.IMAGE_GALLERY.lower():
            raise ValueError(
                f'ImageGallery type must be "{CardType.IMAGE_GALLERY}", not "{v}"'
            )
        return CardType.IMAGE_GALLERY
