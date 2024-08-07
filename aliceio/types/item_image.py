from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class ItemImage(MutableAliceObject):
    """
    Изображение в :class:`ItemsList`

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-itemslist#items-desc)
    """

    image_id: Optional[str] = None  # Optional XD
    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[MediaButton] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            image_id: Optional[str] = None,  # Optional XD
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
