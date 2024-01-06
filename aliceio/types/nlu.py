from typing import Dict, List

from aliceio.types import AliceObject, Entity


Intents = Dict


class NLU(AliceObject):
    """
    Слова и сущности, которые Диалоги извлекли из запроса пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__nlu-desc
    """  # noqa

    tokens: List[str]
    entities: List[Entity]
    intents: Intents
