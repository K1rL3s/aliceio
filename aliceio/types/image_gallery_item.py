from typing import Optional, TYPE_CHECKING, Any

from .base import MutableAliceObject
from .media_button import MediaButton


class ImageGalleryItem(MutableAliceObject):
    """
    Изображение в :class:`ImageGallery`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-desc
    """  # noqa

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
