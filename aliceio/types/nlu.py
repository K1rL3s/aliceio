from typing import Any, Dict, List

from .base import AliceObject
from .entity import Entity

Intents = Dict[str, Any]


class NLU(AliceObject):
    """
    Слова и сущности, которые Диалоги извлекли из запроса пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__nlu-desc
    """  # noqa

    tokens: List[str]
    entities: List[Entity]
    intents: Intents
