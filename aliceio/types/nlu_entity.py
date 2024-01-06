from abc import ABC
from enum import Enum

from aliceio.types import AliceObject


class NLUEntity(ABC, AliceObject):
    """Родителский класс для NLU сущностей"""

    pass


class EntityType(str, Enum):
    YANDEX_FIO = "YANDEX.FIO"
    YANDEX_GEO = "YANDEX.GEO"
    YANDEX_DATETIME = "YANDEX.DATETIME"
    YANDEX_NUMBER = "YANDEX.NUMBER"
