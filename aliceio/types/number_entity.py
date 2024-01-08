from typing import Union

from .base import AliceObject


class NumberEntity(AliceObject):
    """
    NLU Entity Целого или дробного числа

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__number
    """

    value: Union[int, float]
