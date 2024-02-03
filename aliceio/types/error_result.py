from typing import TYPE_CHECKING, Any

from aliceio.types.base import AliceObject


class ErrorResult(AliceObject):
    """
    Сообщение об ошибке при запросах к API Алисы.

    !!! note "Примечание"
        Если навык вернёт ответ Алисе в некорректном формате, то
        Алиса никак не оповестит об ошибке.
    """

    message: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            message: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message=message,
                **__pydantic_kwargs,
            )
