from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict

from aliceio.types import AliceObject


class BaseMiddleware(ABC):
    """Базовый дженерик мидлварь"""

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]],
        event: AliceObject,
        data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Вызов мидлваря

        :param handler: Обёрнутый обработчик в цепочке мидлварей
        :param event: Входящее событие
                      (Подклас :class:`aliceio.types.base.AliceObject`)
        :param data: Данные контекста. Будет сопоставлен с аргументами обработчика.
        :return: :class:`Any`
        """
        pass
