from typing import Optional

from .nlu_entity import NLUEntity


class GeoEntity(NLUEntity):
    """
    NLU Entity Местоположения.

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__geo
    """

    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[int] = None
    airport: Optional[str] = None
