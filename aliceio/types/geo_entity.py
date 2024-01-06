from typing import Optional

from aliceio.types.nlu_entity import NLUEntity


class GeoEntity(NLUEntity):
    """
    NLU Entity Местоположения.

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__geo
    """

    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house_number: Optional[str]
    airport: Optional[str]
