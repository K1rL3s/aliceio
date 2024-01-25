from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from aliceio.fsm.state import State

StateType = Optional[Union[str, State]]

DEFAULT_DESTINY = "default"


@dataclass(frozen=True)
class StorageKey:
    skill_id: str
    user_id: str
    session_id: str
    destiny: str = DEFAULT_DESTINY


class BaseStorage(ABC):
    """Базовый класс для всех FSM хранилищ."""

    @abstractmethod
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Установить состояние по ключу.

        :param key: Ключ.
        :param state: Новое состояние.
        """
        pass

    @abstractmethod
    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Получить состояние по ключу.

        :param key: Ключ.
        :return: Текущее состояние.
        """
        pass

    @abstractmethod
    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Записать данные (перезапись).

        :param key: Ключ.
        :param data: Новые данные.
        """
        pass

    @abstractmethod
    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Получить данные по ключу.

        :param key: Ключ.
        :return: Текущие данные.
        """
        pass

    async def update_data(
        self,
        key: StorageKey,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Обновление данные в хранилище по ключу (like dict.update)

        :param key: Ключ.
        :param data: Часть данных.
        :return: Полные новые данные.
        """
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data.copy()

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Закрыть хранилище (подключение к бд, файлу итп.)
        """
        pass
