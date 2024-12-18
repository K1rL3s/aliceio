from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field, field_validator

from ..enums import CardType
from ..exceptions import AliceWrongFieldError
from .base import MutableAliceObject
from .card_footer import CardFooter
from .card_header import CardHeader
from .item_image import ItemImage


class ItemsList(MutableAliceObject):
    """
    :code:`Card` с типом :code:`ItemsList`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-itemslist)
    """

    type: str = CardType.ITEMS_LIST

    items: list[ItemImage] = Field(
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
            items: list[ItemImage],
            header: Optional[CardHeader] = None,
            footer: Optional[CardFooter] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                items=items,
                header=header,
                footer=footer,
                **__pydantic_kwargs,
            )

    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.ITEMS_LIST.lower():
            raise AliceWrongFieldError(
                f'ItemsList type must be "{CardType.ITEMS_LIST}", not "{v}"',
            )
        return CardType.ITEMS_LIST
