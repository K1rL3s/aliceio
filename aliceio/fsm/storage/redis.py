import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Literal, Optional, cast

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.typing import ExpiryT

from aliceio.fsm.state import State
from aliceio.fsm.storage.base import DEFAULT_DESTINY, BaseStorage, StateType, StorageKey

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class KeyBuilder(ABC):
    """Базовый класс для конструктора ключей Redis."""

    @abstractmethod
    def build(self, key: StorageKey, part: Literal["data", "state"]) -> str:
        """
        Этот метод должен быть реализован в подклассах.

        :param key: Ключ.
        :param part: Часть записи.
        :return: ключ, который будет использоваться в запросах Redis.
        """
        pass


class DefaultKeyBuilder(KeyBuilder):
    """
    Простой конструктор ключей Redis с префиксом по умолчанию.

    Генерирует строку, соединенную через двоеточие,
    с префиксом, user_id, skill_id и destiny.
    """

    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = ":",
        with_destiny: bool = False,
    ) -> None:
        """
        :param prefix: Префикс для всех записей.
        :param separator: Разделитель.
        :param with_destiny: Включая destiny-ключ.
        """
        self.prefix = prefix
        self.separator = separator
        self.with_destiny = with_destiny

    def build(self, key: StorageKey, part: Literal["data", "state"]) -> str:
        parts = [
            self.prefix,
            key.skill_id,
            key.user_id or "",
            key.session_id or "",
            key.application_id or "",
        ]
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Redis key builder is not configured to use key destiny other the default.\n"  # noqa: E501
                "\n"
                "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"  # noqa: E501
                "E.g: `RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))`"  # noqa: E501
            )
        parts.append(part)
        return self.separator.join(parts)


class RedisStorage(BaseStorage):
    """
    Redis storage required :code:`redis` package installed (:code:`pip install redis`)
    """

    def __init__(
        self,
        redis: Redis,
        key_builder: Optional[KeyBuilder] = None,
        state_ttl: Optional[ExpiryT] = None,
        data_ttl: Optional[ExpiryT] = None,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
    ) -> None:
        """
        :param redis: Экземпляр подключения Redis.
        :param key_builder: builder that helps to convert contextual key to string
        :param state_ttl: TTL для записей состояния.
        :param data_ttl: TTL для записей данных.
        :param json_loads: JSON Loads.
        :param json_dumps: JSON Dumps.
        """
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.redis = redis
        self.key_builder = key_builder
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl
        self.json_loads = json_loads
        self.json_dumps = json_dumps

    @classmethod
    def from_url(
        cls,
        url: str,
        connection_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> "RedisStorage":
        """
        Создаёт экземпляр :class:`RedisStorage` по строке подключения.

        :param url: Например, :code:`redis://user:password@host:port/db`
        :param connection_kwargs: см. документацию :code:`redis`.
        :param kwargs: аргументы, которые будут переданы в :class:`RedisStorage`.
        :return: Экземпляр :class:`RedisStorage`
        """
        if connection_kwargs is None:
            connection_kwargs = {}
        pool = ConnectionPool.from_url(url, **connection_kwargs)
        redis = Redis(connection_pool=pool)
        return cls(redis=redis, **kwargs)

    async def close(self) -> None:
        await self.redis.aclose(close_connection_pool=True)

    async def set_state(
        self,
        key: StorageKey,
        state: StateType = None,
    ) -> None:
        redis_key = self.key_builder.build(key, "state")
        if state is None:
            await self.redis.delete(redis_key)
        else:
            await self.redis.set(
                redis_key,
                cast(str, state.state if isinstance(state, State) else state),
                ex=self.state_ttl,
            )

    async def get_state(
        self,
        key: StorageKey,
    ) -> Optional[str]:
        redis_key = self.key_builder.build(key, "state")
        value = await self.redis.get(redis_key)
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return cast(Optional[str], value)

    async def set_data(
        self,
        key: StorageKey,
        data: Dict[str, Any],
    ) -> None:
        redis_key = self.key_builder.build(key, "data")
        if not data:
            await self.redis.delete(redis_key)
            return
        await self.redis.set(
            redis_key,
            self.json_dumps(data),
            ex=self.data_ttl,
        )

    async def get_data(
        self,
        key: StorageKey,
    ) -> Dict[str, Any]:
        redis_key = self.key_builder.build(key, "data")
        value = await self.redis.get(redis_key)
        if value is None:
            return {}
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return cast(Dict[str, Any], self.json_loads(value))
