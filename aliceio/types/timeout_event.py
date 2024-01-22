from typing import TYPE_CHECKING, Any

from .update import Update


class TimeoutUpdate(Update):
    """Внутренннее событие, используется для реакции на выход за время ответа."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(**__pydantic_kwargs)
