from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class CardFooter(MutableAliceObject):
    """
    Текст и кнопки под :class:`ItemsList`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-itemslist#footer-desc)
    """

    text: Optional[str] = None  # Optional XD
    button: Optional[MediaButton] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            text: Optional[str] = None,
            button: Optional[MediaButton] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                text=text,
                button=button,
                **__pydantic_kwargs,
            )
