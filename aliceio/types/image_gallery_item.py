from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class ImageGalleryItem(MutableAliceObject):
    """
    Изображение в :class:`ImageGallery`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-imagegallery#items-desc)
    """

    image_id: str
    title: Optional[str] = None
    button: Optional[MediaButton] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            image_id: str,
            title: Optional[str] = None,
            button: Optional[MediaButton] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                image_id=image_id,
                title=title,
                button=button,
                **__pydantic_kwargs,
            )
