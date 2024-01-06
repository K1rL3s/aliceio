from typing import Optional

from aliceio.types.nlu_entity import NLUEntity


class FIOEntity(NLUEntity):
    """
    NLU Entity Фамилии, имени и отчества.

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__fio
    """

    first_name: Optional[str] = None
    patronymic_name: Optional[str] = None
    last_name: Optional[str] = None
