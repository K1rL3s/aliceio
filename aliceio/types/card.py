from abc import ABC
from enum import Enum

from pydantic import field_validator

from aliceio.types import AliceObject


class Card(ABC, AliceObject):
    """
    Родительский класс для карт
    :class:`BigImage`, :class:`ImageGallery` и :class:`ItemsList`
    """

    type: str

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v not in CardType:
            raise ValueError(
                f'Card "type" must be '
                f'{", ".join(ctype for ctype in CardType)}, not "{v}"'
            )
        return v


class CardType(str, Enum):
    BIG_IMAGE = "BigImage"
    IMAGE_GALLERY = "ImageGallery"
    ITEMS_LIST = "ItemsList"
