from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .payload import Payload


class TextButton(MutableAliceObject):
    """
    Кнопка под сообщением навыка или над клавиатурой пользователя.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/response.html#response__buttons-desc)
    """

    title: str
    url: Optional[str] = None
    payload: Optional[Payload] = None
    hide: bool = True

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            title: str,
            url: Optional[str] = None,
            payload: Optional[Payload] = None,
            hide: bool = True,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                title=title,
                url=url,
                payload=payload,
                hide=hide,
                **__pydantic_kwargs,
            )
