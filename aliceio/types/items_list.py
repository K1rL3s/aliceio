from typing import List, Optional

from pydantic import field_validator

from ..enums.card import CardType
from .card import Card
from .card_footer import CardFooter
from .card_header import CardHeader
from .item_image import ItemImage


class ItemsList(Card):
    """
    :class:`Card` с типом :code:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html
    """

    type: str = CardType.ITEMS_LIST

    header: Optional[CardHeader] = None
    items: Optional[List[ItemImage]] = None
    footer: Optional[CardFooter] = None

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.ITEMS_LIST.lower():
            raise ValueError(
                f'ItemsList type must be "{CardType.ITEMS_LIST}", not "{v}"'
            )
        return CardType.ITEMS_LIST
