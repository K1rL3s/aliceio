from typing import Any, Dict

from .base import MutableAliceObject

CustomEventData = Dict[str, Any]


class Event(MutableAliceObject):
    """
    Событие для аналитики.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__events-desc
    """

    name: str
    value: CustomEventData
