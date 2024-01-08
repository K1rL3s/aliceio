from abc import ABC

from pydantic import field_validator

from .base import MutableAliceObject
from ..enums.card import CardType


class Card(MutableAliceObject, ABC):
    """
    Родительский класс для карт
    :class:`BigImage`, :class:`ImageGallery` и :class:`ItemsList`
    """

    type: str

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v not in CardType.values():
            raise ValueError(
                f'Card "type" must be '
                f'{", ".join(ctype for ctype in CardType)}, not "{v}"'
            )
        return v
