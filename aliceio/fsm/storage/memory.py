from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Any, Optional, overload

from aliceio.fsm.state import State
from aliceio.fsm.storage.base import BaseStorage, StateType, StorageKey


@dataclass
class MemoryStorageRecord:
    data: dict[str, Any] = field(default_factory=dict)
    state: Optional[str] = None


class MemoryStorage(BaseStorage):
    """
    FSM хранилище по умолчанию,
    хранит все данные в :class:`dict` и теряет всё при выключении.

    !!! warning "Важно"
        Не рекомендуется использовать в проде,
        так как данные теряются при перезапуске навыка.
    """

    def __init__(self) -> None:
        self.storage: defaultdict[StorageKey, MemoryStorageRecord] = defaultdict(
            MemoryStorageRecord,
        )

    async def close(self) -> None:
        pass

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        self.storage[key].state = state.state if isinstance(state, State) else state

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return self.storage[key].state

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        self.storage[key].data = data.copy()

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        return self.storage[key].data.copy()

    @overload
    async def get_value(
        self,
        storage_key: StorageKey,
        dict_key: str,
    ) -> Optional[Any]: ...

    @overload
    async def get_value(
        self,
        storage_key: StorageKey,
        dict_key: str,
        default: Any,
    ) -> Any: ...

    async def get_value(
        self,
        storage_key: StorageKey,
        dict_key: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        data = self.storage[storage_key].data
        return copy(data.get(dict_key, default))
