from typing import TYPE_CHECKING, Any, Optional

from .nlu_entity import NLUNamedEntity


class GeoEntity(NLUNamedEntity):
    """
    NLU Entity Местоположения.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/naming-entities#geo)
    """

    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None  # str по доке
    airport: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            country: Optional[str] = None,
            city: Optional[str] = None,
            street: Optional[str] = None,
            house_number: Optional[str] = None,
            airport: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                country=country,
                city=city,
                street=street,
                house_number=house_number,
                airport=airport,
                **__pydantic_kwargs,
            )
