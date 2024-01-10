from typing import Optional

from pydantic import field_validator

from ..enums import CardType
from .card import Card
from .media_button import MediaButton


class BigImage(Card):
    """
    :class:`Card` с типом :code:`BigImage`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-bigimage.html
    """

    type: str = CardType.BIG_IMAGE

    image_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[MediaButton] = None

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.BIG_IMAGE.lower():
            raise ValueError(f'BigImage type must be "{CardType.BIG_IMAGE}", not "{v}"')
        return CardType.BIG_IMAGE
