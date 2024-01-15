from typing import Optional, TYPE_CHECKING, Any

from pydantic import field_validator

from ..enums import CardType
from .base import MutableAliceObject
from .media_button import MediaButton


class BigImage(MutableAliceObject):
    """
    :code:`Card` с типом :code:`BigImage`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-bigimage.html
    """

    type: str = CardType.BIG_IMAGE

    image_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[MediaButton] = None

    if TYPE_CHECKING:
        def __init__(
            __pydantic_self__,
            *,
            image_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            button: Optional[MediaButton] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                image_id=image_id,
                title=title,
                description=description,
                button=button,
                **__pydantic_kwargs,
            )


    @field_validator("type")
    @classmethod
    def type_validate(cls, v: str) -> str:
        if v.lower() != CardType.BIG_IMAGE.lower():
            raise ValueError(f'BigImage type must be "{CardType.BIG_IMAGE}", not "{v}"')
        return CardType.BIG_IMAGE
