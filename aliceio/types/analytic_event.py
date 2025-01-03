from typing import TYPE_CHECKING, Any

from .base import MutableAliceObject

CustomEventData = dict[str, Any]


class AnalyticEvent(MutableAliceObject):
    """
    Событие для аналитики.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response#events-desc)
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
