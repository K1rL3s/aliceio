from collections.abc import Sequence
from inspect import isclass
from typing import Any, Optional, Union, cast

from aliceio.filters.base import Filter
from aliceio.fsm.state import State, StatesGroup
from aliceio.types.base import AliceObject

StateType = Union[str, None, State, StatesGroup, type[StatesGroup]]


class StateFilter(Filter):
    """Фильтр по состоянию."""

    __slots__ = ("states",)

    def __init__(self, *states: StateType) -> None:
        """
        :param states: Состояния, на которые должен реагировать фильтр.
        """
        if not states:
            raise ValueError("At least one state is required")

        self.states = states

    def __str__(self) -> str:
        return self._signature_to_string(*self.states)

    async def __call__(
        self,
        obj: AliceObject,
        raw_state: Optional[str] = None,
    ) -> Union[bool, dict[str, Any]]:
        allowed_states = cast(Sequence[StateType], self.states)
        for allowed_state in allowed_states:
            if isinstance(allowed_state, str) or allowed_state is None:
                if allowed_state == "*" or raw_state == allowed_state:
                    return True
            elif isinstance(allowed_state, (State, StatesGroup)):
                if allowed_state(event=obj, raw_state=raw_state):
                    return True
            elif isclass(allowed_state) and issubclass(allowed_state, StatesGroup):
                if allowed_state()(event=obj, raw_state=raw_state):
                    return True
        return False
