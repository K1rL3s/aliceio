from typing import Any, Optional, overload

from aliceio.fsm.storage.base import BaseStorage, StateType, StorageKey


class FSMContext:
    """
    Класс для доступа к информации состояния конкретного пользователя.
    Создаётся и передаётся в обработчики при каждом событии.
    """

    def __init__(self, storage: BaseStorage, key: StorageKey) -> None:
        """
        :param storage: Хранилище -> BaseStorage.
        :param key: Ключ.
        """
        self.storage = storage
        self.key = key

    async def set_state(self, state: StateType = None) -> None:
        """
        Установить состояние по ключу.

        :param state: Новое состояние.
        """
        await self.storage.set_state(key=self.key, state=state)

    async def get_state(self) -> Optional[str]:
        """
        Получить состояние по ключу.

        :return: Текущее состояние.
        """
        return await self.storage.get_state(key=self.key)

    async def set_data(
        self,
        data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Записать данные (перезапись).

        :param data: Новые данные.
        """
        if data:
            kwargs.update(data)
        await self.storage.set_data(key=self.key, data=kwargs)

    async def get_data(self) -> dict[str, Any]:
        """
        Получить данные по ключу.

        :return: Текущие данные.
        """
        return await self.storage.get_data(key=self.key)

    @overload
    async def get_value(self, key: str) -> Optional[Any]: ...

    @overload
    async def get_value(self, key: str, default: Any) -> Any: ...

    async def get_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return await self.storage.get_value(
            storage_key=self.key,
            dict_key=key,
            default=default,
        )

    async def update_data(
        self,
        data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Обновление данные в хранилище по ключу (like dict.update)

        :param data: Часть данных.
        :return: Полные новые данные.
        """
        if data:
            kwargs.update(data)
        return await self.storage.update_data(key=self.key, data=kwargs)

    async def clear(self) -> None:
        """
        Очистить состояние и данные.
        """
        await self.set_state(state=None)
        await self.set_data({})
