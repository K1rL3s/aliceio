from typing import List, Optional

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
