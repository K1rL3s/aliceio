from typing import List

from .base import MutableAliceObject
from .event import Event


class Analytics(MutableAliceObject):
    """
    Данные для аналитики AppMetrica.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__analytics-desc
    """

    events: List[Event]
