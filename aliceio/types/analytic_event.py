from typing import TYPE_CHECKING, Any, Dict

from .base import MutableAliceObject

CustomEventData = Dict[str, Any]


class AnalyticEvent(MutableAliceObject):
    """
    Событие для аналитики.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__events-desc
    """

    name: str
    value: CustomEventData

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            name: str,
            value: CustomEventData,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                name=name,
                value=value,
                **__pydantic_kwargs,
            )
