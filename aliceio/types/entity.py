from typing import TYPE_CHECKING, Any, Optional, Union

from ..enums.entity import EntityType
from .base import MutableAliceObject
from .datetime import DateTimeEntity
from .fio_entity import FIOEntity
from .geo_entity import GeoEntity
from .nlu_entity import NLUNamedEntity
from .number_entity import NumberEntity
from .tokens_entity import EntityTokens

NLUEntityType = Union[
    NLUNamedEntity,
    DateTimeEntity,
    FIOEntity,
    GeoEntity,
    NumberEntity,
]
EntityValue = Optional[Union[NLUEntityType, Any]]


class Entity(MutableAliceObject):
    """
    NLU Entity

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/naming-entities)
    """

    type: str
    tokens: EntityTokens
    value: EntityValue = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            tokens: EntityTokens,
            value: EntityValue = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                tokens=tokens,
                value=value,
                **__pydantic_kwargs,
            )

    def model_post_init(self, context: Any, /) -> None:
        super().model_post_init(context)

        if self.value is None or isinstance(self.value, (int, float)):
            # "YANDEX.NUMBER" или пустое
            return

        entity_type: dict[str, type[NLUNamedEntity]] = {
            EntityType.YANDEX_FIO: FIOEntity,
            EntityType.YANDEX_GEO: GeoEntity,
            EntityType.YANDEX_DATETIME: DateTimeEntity,
        }
        if known_entity := entity_type.get(self.type):
            self.value = known_entity.model_validate(self.value, from_attributes=True)
