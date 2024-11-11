from typing import TYPE_CHECKING, Any

from .base import AliceObject
from .entity import Entity

Intents = dict[str, Any]


class NLU(AliceObject):
    """
    Слова и сущности, которые Диалоги извлекли из запроса пользователя.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request-simpleutterance#nlu-desc)
    """

    tokens: list[str]
    entities: list[Entity]
    intents: Intents

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            tokens: list[str],
            entities: list[Entity],
            intents: Intents,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                tokens=tokens,
                entities=entities,
                intents=intents,
                **__pydantic_kwargs,
            )
