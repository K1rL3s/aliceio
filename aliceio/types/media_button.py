from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .payload import Payload


class MediaButton(MutableAliceObject):
    """
    Кнопка на изображении из :class:[`ImageGallery`](https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-button-desc) и :class:[`ItemsList`](https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-button-desc).
    """  # noqa: E501

    text: str
    url: str
    payload: Optional[Payload] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            text: str,
            url: str,
            payload: Optional[Payload] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                text=text,
                url=url,
                payload=payload,
                **__pydantic_kwargs,
            )
