from typing import TYPE_CHECKING, Any, Optional

from .nlu_entity import NLUEntity


class GeoEntity(NLUEntity):
    """
    [NLU Entity](https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__geo) Местоположения.
    """

    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[int] = None
    airport: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            country: Optional[str] = None,
            city: Optional[str] = None,
            street: Optional[str] = None,
            house_number: Optional[int] = None,
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
