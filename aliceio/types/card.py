from abc import ABC

from pydantic import field_validator

from ..enums import CardType
from .base import MutableAliceObject


class Card(MutableAliceObject, ABC):
    """
    Родительский класс для карт
    :class:`BigImage`, :class:`ImageGallery` и :class:`ItemsList`
    """

    type: str

    @field_validator("type", mode="after")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v not in CardType.values():
            raise ValueError(
                f'Card "type" must be '
                f'{", ".join(ctype for ctype in CardType)}, not "{v}"'
            )
        return v
