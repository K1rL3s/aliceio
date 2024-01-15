from typing import TYPE_CHECKING, Any, Optional

from .base import AliceObject


class User(AliceObject):
    """
    Пользователь из :class:`Session`.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__user-desc
    """

    user_id: str
    access_token: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            user_id: str,
            access_token: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                user_id=user_id,
                access_token=access_token,
                **__pydantic_kwargs,
            )
