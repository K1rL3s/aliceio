from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Generic, TypeVar

from aliceio.types.base import AliceObject

EventType = TypeVar("EventType", bound=AliceObject)


class BaseMiddleware(ABC, Generic[EventType]):
    """Базовый дженерик мидлварь"""

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[EventType, Dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Вызов мидлваря

        :param handler: Обёрнутый обработчик в цепочке мидлварей
        :param event: Входящее событие
            (Подкласс :class:`aliceio.types.base.AliceObject`)
        :param data: Данные контекста. Будет сопоставлен с аргументами обработчика.
        :return: :class:`Any`
        """
        pass
