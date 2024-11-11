from collections.abc import Iterable
from copy import copy
from inspect import isclass
from typing import Optional, Union

import pytest

from aliceio.dispatcher.event.handler import FilterObject
from aliceio.filters import StateFilter
from aliceio.fsm.state import State, StatesGroup
from aliceio.types import AliceRequest


class MyGroup(StatesGroup):
    state = State()


class TestStateFilter:
    @pytest.mark.parametrize(
        "state",
        [None, State("test"), MyGroup, MyGroup(), "state"],
    )
    def test_validator(self, state) -> None:
        f = StateFilter(state)
        assert isinstance(f.states, tuple)
        value = f.states[0]
        assert (
            isinstance(value, (State, str, MyGroup))
            or (isclass(value) and issubclass(value, StatesGroup))
            or value is None
        )

    @pytest.mark.parametrize(
        "state,current_state,result",
        [
            [[State("state")], "@:state", True],
            [[MyGroup], "MyGroup:state", True],
            [[MyGroup()], "MyGroup:state", True],
            [["*"], "state", True],
            [[None], None, True],
            [[State("state"), "state"], "state", True],
            [[MyGroup(), State("state")], "@:state", True],
            [[MyGroup, State("state")], "state", False],
        ],
    )
    async def test_filter(
        self,
        state: Iterable[Union[str, None, State, StatesGroup, type[StatesGroup]]],
        current_state: Optional[str],
        result: bool,
        event: AliceRequest,
    ) -> None:
        f = StateFilter(*state)
        test_result = bool(await f(obj=event, raw_state=current_state))
        assert test_result is result

    def test_empty_filter(self) -> None:
        with pytest.raises(ValueError):
            StateFilter()

    async def test_create_filter_from_state(self) -> None:
        FilterObject(callback=State(state="state"))

    async def test_state_copy(self) -> None:
        class SG(StatesGroup):
            state = State()

        assert SG.state == copy(SG.state)

        assert SG.state == "SG:state"
        assert SG.state == "SG:state"

        assert State() == State()
        assert SG.state != 1

        states = {SG.state: "OK"}
        assert states.get(copy(SG.state)) == "OK"

    def test_str(self) -> None:
        f = StateFilter("test")
        assert str(f) == "StateFilter('test')"
