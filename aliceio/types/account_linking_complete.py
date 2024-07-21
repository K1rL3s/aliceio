from typing import TYPE_CHECKING, Any

from .base import MutableAliceObject


class AccountLinkingComplete(MutableAliceObject):
    """
    Успешная авторизация пользователя в навыке.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/auth/make-skill#authorization-complete)
    """

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                **__pydantic_kwargs,
            )
