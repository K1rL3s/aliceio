from typing import TYPE_CHECKING, Any

from .base import AliceObject
from .update import Update


class ErrorEvent(AliceObject):
    """Внутренннее событие, используется для получения ошибок при обработке событий."""

    update: Update
    exception: Exception

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            update: Update,
            exception: Exception,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                update=update,
                exception=exception,
                **__pydantic_kwargs,
            )
