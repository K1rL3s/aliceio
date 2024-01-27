from typing import TYPE_CHECKING, Any, List

from .analytic_event import AnalyticEvent
from .base import MutableAliceObject


class Analytics(MutableAliceObject):
    """
    [Данные](https://yandex.ru/dev/dialogs/alice/doc/response.html#response__analytics-desc) для аналитики AppMetrica.
    """

    events: List[AnalyticEvent]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            events: List[AnalyticEvent],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                events=events,
                **__pydantic_kwargs,
            )
