from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any, Callable, Generic, TypeVar

from aliceio.types.base import AliceObject

EventType = TypeVar("EventType", bound=AliceObject)


class BaseMiddleware(ABC, Generic[EventType]):
    """Базовый дженерик мидлварь"""

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[EventType, dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Вызов мидлваря

        :param handler: Обёрнутый обработчик в цепочке мидлварей
        :param event: Входящее событие
            (Подкласс :class:`aliceio.types.base.AliceObject`)
        :param data: Данные контекста. Будет сопоставлен с аргументами обработчика.
        :return: :class:`Any`
        """
