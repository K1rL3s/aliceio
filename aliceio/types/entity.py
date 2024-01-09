from typing import Any, Dict, Optional, Type, Union

from ..enums.entity import EntityType
from .base import MutableAliceObject
from .datetime import DateTimeEntity
from .fio_entity import FIOEntity
from .geo_entity import GeoEntity
from .nlu_entity import NLUEntity
from .number_entity import NumberEntity
from .tokens_entity import TokensEntity


class Entity(MutableAliceObject):
    """
    NLU Entity

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__entities-desc
    """  # noqa

    type: str
    tokens: TokensEntity
    value: Optional[Union[NLUEntity, NumberEntity]] = None

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if not self.value or isinstance(self.value, (int, float)):  # "YANDEX.NUMBER"
            return
        entity_type: Dict[str, Type[NLUEntity]] = {
            EntityType.YANDEX_FIO: FIOEntity,
            EntityType.YANDEX_GEO: GeoEntity,
            EntityType.YANDEX_DATETIME: DateTimeEntity,
        }
        if (known_entity := entity_type.get(self.type)) is None:
            return
        self.value = known_entity.model_validate(self.value, from_attributes=True)