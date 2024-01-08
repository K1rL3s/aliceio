from typing import Dict, Optional, Type, cast

from ..enums.entity import EntityType
from .base import AliceObject
from .datetime import DateTimeEntity
from .fio_entity import FIOEntity
from .geo_entity import GeoEntity
from .nlu_entity import NLUEntity
from .number_entity import NumberEntity
from .tokens_entity import TokensEntity


class Entity(AliceObject):
    """
    NLU Entity

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__entities-desc
    """  # noqa

    type: str
    tokens: TokensEntity
    value: Optional[NLUEntity] = None

    def __post_init__(self):
        if not self.value:
            return
        entity_type: Dict[str, Type[NLUEntity]] = {
            EntityType.YANDEX_FIO: FIOEntity,
            EntityType.YANDEX_GEO: GeoEntity,
            EntityType.YANDEX_DATETIME: DateTimeEntity,
            EntityType.YANDEX_NUMBER: NumberEntity,
        }
        self.value = entity_type.get(self.type, dict)(**cast(dict, self.value))
