from typing import TYPE_CHECKING, Any

from aliceio.types.base import AliceObject


class Result(AliceObject):
    """
    Ответ на удаление файла.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload#delete)
    """

    result: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            result: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                result=result,
                **__pydantic_kwargs,
            )
