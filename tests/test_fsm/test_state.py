import sys

import pytest

from aliceio.fsm.state import State, StatesGroup, any_state
from aliceio.types.base import AliceObject

PY312_OR_GREATER = sys.version_info >= (3, 12)


class TestState:
    def test_empty(self) -> None:
        state = State()
        assert state._state is None
        assert state._group_name is None
        assert state._group is None

        with pytest.raises(RuntimeError):
            assert state.group

        assert state.state is None
        assert str(state) == "<State ''>"

    def test_star(self) -> None:
        state = State(state="*")
        assert state._state == "*"
        assert state._group_name is None
        assert state._group is None

        with pytest.raises(RuntimeError):
            assert state.group
        assert state.state == "*"
        assert str(state) == "<State '*'>"

    def test_star_filter(self) -> None:
        assert any_state(AliceObject(), "foo")
        assert any_state(AliceObject(), "bar")
        assert any_state(AliceObject(), "baz")

    def test_alone(self) -> None:
        state = State("test")
        assert state._state == "test"
        assert state._group_name is None
        assert state._group is None

        with pytest.raises(RuntimeError):
            assert state.group

        assert state.state == "@:test"
        assert str(state) == "<State '@:test'>"

    def test_alone_with_group(self) -> None:
        state = State("test", group_name="Test")
        assert state._state == "test"
        assert state._group_name == "Test"
        assert state._group is None

        with pytest.raises(RuntimeError):
            assert state.group == "Test"

        assert state.state == "Test:test"
        assert str(state) == "<State 'Test:test'>"

    @pytest.mark.parametrize(
        "state,check,result",
        [
            [State("test"), "test", False],
            [State("test"), "@:test", True],
            [State("test"), "test1", False],
            [State("test", group_name="test"), "test:test", True],
            [State("test", group_name="test"), "test:test2", False],
            [State("test", group_name="test"), "test2:test", False],
            [State("test", group_name="test"), "test2:test2", False],
        ],
    )
    def test_filter(self, state: State, check: str, result: bool) -> None:
        assert state(AliceObject(), check) is result

    def test_state_in_unknown_class(self) -> None:
        if PY312_OR_GREATER:
            # Python 3.12+ does not wrap
            # __set_name__ exceptions with RuntimeError anymore as part
            # of PEP 678. See "Other Language Changes" in the changelogs:
            # https://docs.python.org/3/whatsnew/3.12.html
            with pytest.raises(ValueError):

                class MyClass:
                    state1 = State()

        else:
            with pytest.raises(RuntimeError):

                class MyClass:
                    state1 = State()


class TestStatesGroup:
    def test_empty(self) -> None:
        class MyGroup(StatesGroup):
            pass

        assert MyGroup.__states__ == ()
        assert MyGroup.__state_names__ == ()
        assert MyGroup.__all_childs__ == ()
        assert MyGroup.__all_states__ == ()
        assert MyGroup.__all_states_names__ == ()
        assert MyGroup.__parent__ is None
        assert MyGroup.__full_group_name__ == "MyGroup"

        assert str(MyGroup) == "<StatesGroup 'MyGroup'>"

    def test_with_state(self) -> None:
        class MyGroup(StatesGroup):
            state1 = State()

        assert MyGroup.__states__ == (MyGroup.state1,)
        assert MyGroup.__state_names__ == ("MyGroup:state1",)
        assert MyGroup.__all_childs__ == ()
        assert MyGroup.__all_states__ == (MyGroup.state1,)
        assert MyGroup.__parent__ is None
        assert MyGroup.__full_group_name__ == "MyGroup"

        assert str(MyGroup) == "<StatesGroup 'MyGroup'>"

        assert MyGroup.state1.state == "MyGroup:state1"
        assert MyGroup.state1.group == MyGroup

    def test_nested_group(self) -> None:
        class MyGroup(StatesGroup):
            state1 = State()

            class MyNestedGroup(StatesGroup):
                state1 = State()

        assert MyGroup.__states__ == (MyGroup.state1,)
        assert MyGroup.__state_names__ == ("MyGroup:state1",)
        assert MyGroup.__all_childs__ == (MyGroup.MyNestedGroup,)
        assert MyGroup.__all_states__ == (MyGroup.state1, MyGroup.MyNestedGroup.state1)
        assert MyGroup.__parent__ is None
        assert MyGroup.MyNestedGroup.__parent__ is MyGroup
        assert MyGroup.__full_group_name__ == "MyGroup"
        assert MyGroup.MyNestedGroup.__full_group_name__ == "MyGroup.MyNestedGroup"

        assert str(MyGroup) == "<StatesGroup 'MyGroup'>"
        assert str(MyGroup.MyNestedGroup) == "<StatesGroup 'MyGroup.MyNestedGroup'>"

        assert MyGroup.state1.state == "MyGroup:state1"
        assert MyGroup.state1.group == MyGroup

        assert MyGroup.MyNestedGroup.state1.state == "MyGroup.MyNestedGroup:state1"
        assert MyGroup.MyNestedGroup.state1.group == MyGroup.MyNestedGroup

        assert MyGroup.MyNestedGroup.state1 in MyGroup.MyNestedGroup
        assert MyGroup.MyNestedGroup.state1 in MyGroup
        assert MyGroup.state1 not in MyGroup.MyNestedGroup
        assert MyGroup.state1 in MyGroup

        assert MyGroup.MyNestedGroup in MyGroup

        assert "MyGroup.MyNestedGroup:state1" in MyGroup
        assert "MyGroup.MyNestedGroup:state1" in MyGroup.MyNestedGroup

        assert MyGroup.state1 not in MyGroup.MyNestedGroup
        assert "test" not in MyGroup
        assert 42 not in MyGroup

        assert MyGroup.MyNestedGroup.get_root() is MyGroup

    def test_iterable(self) -> None:
        class Group(StatesGroup):
            x = State()
            y = State()

        assert set(Group) == {Group.x, Group.y}

    def test_empty_filter(self) -> None:
        class MyGroup(StatesGroup):
            pass

        assert str(MyGroup()) == "StatesGroup MyGroup"

    def test_with_state_filter(self) -> None:
        class MyGroup(StatesGroup):
            state1 = State()
            state2 = State()

        assert MyGroup()(AliceObject(), "MyGroup:state1")
        assert MyGroup()(AliceObject(), "MyGroup:state2")
        assert not MyGroup()(AliceObject(), "MyGroup:state3")

        assert str(MyGroup()) == "StatesGroup MyGroup"

    def test_nested_group_filter(self) -> None:
        class MyGroup(StatesGroup):
            state1 = State()

            class MyNestedGroup(StatesGroup):
                state1 = State()

        assert MyGroup()(AliceObject(), "MyGroup:state1")
        assert MyGroup()(AliceObject(), "MyGroup.MyNestedGroup:state1")
        assert not MyGroup()(AliceObject(), "MyGroup:state2")
        assert MyGroup.MyNestedGroup()(AliceObject(), "MyGroup.MyNestedGroup:state1")
        assert not MyGroup.MyNestedGroup()(AliceObject(), "MyGroup:state1")

        assert str(MyGroup()) == "StatesGroup MyGroup"
        assert str(MyGroup.MyNestedGroup()) == "StatesGroup MyGroup.MyNestedGroup"
