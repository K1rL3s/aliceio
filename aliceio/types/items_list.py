from typing import List, Optional

from aliceio.types import Card, CardType, ItemImage, CardHeader, CardFooter


class ItemsList(Card):
    """
    :class:`Card` с типом :code:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html
    """

    type: str = CardType.ITEMS_LIST

    header: Optional[CardHeader] = None
    items: Optional[List[ItemImage]] = None
    footer: Optional[CardFooter] = None
