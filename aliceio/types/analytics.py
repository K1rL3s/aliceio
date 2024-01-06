from typing import List

from aliceio.types import AliceObject
from aliceio.types.event import Event


class Analytics(AliceObject):
    """
    Данные для аналитики AppMetrica.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__analytics-desc
    """

    events: List[Event]
