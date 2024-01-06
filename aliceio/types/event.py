from typing import Dict

from aliceio.types import AliceObject


CustomEventData = Dict


class Event(AliceObject):
    """
    Событие для аналитики.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__events-desc
    """

    name: str
    value: CustomEventData
