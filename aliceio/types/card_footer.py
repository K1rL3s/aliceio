from typing import Optional, TYPE_CHECKING, Any

from .base import MutableAliceObject
from .media_button import MediaButton


class CardFooter(MutableAliceObject):
    """
    Текст и кнопки под :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__footer-desc
    """  # noqa

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
