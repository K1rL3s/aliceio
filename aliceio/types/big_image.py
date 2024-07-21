from typing import TYPE_CHECKING, Any, Optional

from pydantic import field_validator

from ..enums import CardType
from ..exceptions import AliceWrongFieldError
from .base import MutableAliceObject
from .media_button import MediaButton


class BigImage(MutableAliceObject):
    """
    :code:`Card` с типом :code:`BigImage`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-bigimage)
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
            raise AliceWrongFieldError(
                f'BigImage type must be "{CardType.BIG_IMAGE}", not "{v}"',
            )
        return CardType.BIG_IMAGE
