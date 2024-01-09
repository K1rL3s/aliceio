from typing import List

from .analytic_event import AnalyticEvent
from .base import MutableAliceObject


class Analytics(MutableAliceObject):
    """
    Данные для аналитики AppMetrica.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__analytics-desc
    """

    events: List[AnalyticEvent]
