from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import Field, field_validator

from ..enums import CardType
from .base import MutableAliceObject
from .card_footer import CardFooter
from .card_header import CardHeader
from .item_image import ItemImage


class ItemsList(MutableAliceObject):
    """
    :code:`Card` с типом :code:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html
    """

    type: str = CardType.ITEMS_LIST

    items: List[ItemImage] = Field(
        default_factory=list,
        min_length=1,
        max_length=5,
    )
    header: Optional[CardHeader] = None
    footer: Optional[CardFooter] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            items: List[ItemImage],
            header: Optional[CardHeader] = None,
            footer: Optional[CardFooter] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                items=items,
                header=header,
                footer=footer,
                **__pydantic_kwargs,
            )

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.ITEMS_LIST.lower():
            raise ValueError(
                f'ItemsList type must be "{CardType.ITEMS_LIST}", not "{v}"'
            )
        return CardType.ITEMS_LIST
