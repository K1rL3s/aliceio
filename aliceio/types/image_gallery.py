from typing import TYPE_CHECKING, Any, List

from pydantic import Field, field_validator

from ..enums import CardType
from ..exceptions import AliceWrongFieldError
from .base import MutableAliceObject
from .image_gallery_item import ImageGalleryItem


class ImageGallery(MutableAliceObject):
    """
    :code:`Card` с типом :code:`ImageGallery`

    [Source](https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html)
    """

    type: str = CardType.IMAGE_GALLERY
    items: List[ImageGalleryItem] = Field(
        default_factory=list,
        min_length=1,
        max_length=10,
    )

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            items: List[ImageGalleryItem],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                items=items,
                **__pydantic_kwargs,
            )

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.IMAGE_GALLERY.lower():
            raise AliceWrongFieldError(
                f'ImageGallery type must be "{CardType.IMAGE_GALLERY}", not "{v}"'
            )
        return CardType.IMAGE_GALLERY
