from typing import TYPE_CHECKING, Any

from .base import AliceObject


class TokensEntity(AliceObject):
    """
    start и end из [request.nlu.entities](https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__entities-desc).
    """  # noqa: E501

    start: int
    end: int

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            start: int,
            end: int,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                start=start,
                end=end,
                **__pydantic_kwargs,
            )
