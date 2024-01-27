from typing import TYPE_CHECKING, Any, Dict, List

from .base import AliceObject
from .entity import Entity

Intents = Dict[str, Any]


class NLU(AliceObject):
    """
    [Слова и сущности](https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__nlu-desc), которые Диалоги извлекли из запроса пользователя.
    """  # noqa: E501

    tokens: List[str]
    entities: List[Entity]
    intents: Intents

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            tokens: List[str],
            entities: List[Entity],
            intents: Intents,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                tokens=tokens,
                entities=entities,
                intents=intents,
                **__pydantic_kwargs,
            )
