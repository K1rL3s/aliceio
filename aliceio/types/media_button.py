from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .payload import Payload


class MediaButton(MutableAliceObject):
    """
    Кнопка на изображении для :class:`ImageGallery` и :class:`ItemsList`

    [Source 1](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-imagegallery#items-button-desc)

    [Source 2](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-itemslist#items-button-desc)
    """

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
