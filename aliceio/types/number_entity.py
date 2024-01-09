from typing import Union

from .nlu_entity import NLUEntity


class NumberEntity(NLUEntity):
    """
    NLU Entity Целого или дробного числа

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__number
    """

    value: Union[int, float]
