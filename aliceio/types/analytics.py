from typing import TYPE_CHECKING, Any

from .analytic_event import AnalyticEvent
from .base import MutableAliceObject


class Analytics(MutableAliceObject):
    """
    Данные для аналитики AppMetrica.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response#analytics-desc)
    """

    events: list[AnalyticEvent]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            events: list[AnalyticEvent],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                events=events,
                **__pydantic_kwargs,
            )
