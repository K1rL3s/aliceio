import logging
from typing import cast, Dict, Optional, Type

from pydantic import field_validator

from aliceio.types import AliceObject, TokensEntity
from aliceio.types.datetime import DateTimeEntity
from aliceio.types.fio_entity import FIOEntity
from aliceio.types.geo_entity import GeoEntity
from aliceio.types.number_entity import NumberEntity
from aliceio.types.nlu_entity import NLUEntity, EntityType


log = logging.getLogger(__name__)


class Entity(AliceObject):
    """
    NLU Entity

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__entities-desc
    """  # noqa

    type: str
    tokens: TokensEntity
    value: Optional[NLUEntity] = None

    @field_validator("type")
    def check(self, v: str) -> str:
        """Report unknown type"""
        if v not in EntityType:
            log.error('Unknown Entity type! "%r"', v)
        return v

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
