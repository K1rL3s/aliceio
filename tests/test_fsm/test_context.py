import pytest

from aliceio.fsm.context import FSMContext
from aliceio.fsm.storage.base import DEFAULT_DESTINY, StorageKey
from aliceio.fsm.storage.memory import MemoryStorage
from tests.mocked import MockedSkill


@pytest.fixture()
def state(skill: MockedSkill):
    storage = MemoryStorage()
    key = StorageKey(
        skill_id=skill.id,
        user_id="42:USER_ID",
        session_id="42:SESSION_ID",
        destiny=DEFAULT_DESTINY,
    )
    ctx = storage.storage[key]
    ctx.state = "test"
    ctx.data = {"foo": "bar"}
    return FSMContext(storage=storage, key=key)


class TestFSMContext:
    async def test_address_mapping(self, skill: MockedSkill):
        storage = MemoryStorage()
        ctx = storage.storage[
            StorageKey(session_id="-42", user_id="42", skill_id=skill.id)
        ]
        ctx.state = "test"
        ctx.data = {"foo": "bar"}
        state = FSMContext(
            storage=storage,
            key=StorageKey(
                session_id="-42",
                user_id="42",
                skill_id=skill.id,
            ),
        )
        state2 = FSMContext(
            storage=storage,
            key=StorageKey(
                session_id="42",
                user_id="42",
                skill_id=skill.id,
            ),
        )
        state3 = FSMContext(
            storage=storage,
            key=StorageKey(
                session_id="69",
                user_id="69",
                skill_id=skill.id,
            ),
        )

        assert await state.get_state() == "test"
        assert await state2.get_state() is None
        assert await state3.get_state() is None

        assert await state.get_data() == {"foo": "bar"}
        assert await state2.get_data() == {}
        assert await state3.get_data() == {}

        await state2.set_state("experiments")
        assert await state.get_state() == "test"
        assert await state3.get_state() is None

        await state3.set_data({"key": "value"})
        assert await state2.get_data() == {}

        await state.update_data({"key": "value"})
        assert await state.get_data() == {"foo": "bar", "key": "value"}

        await state.clear()
        assert await state.get_state() is None
        assert await state.get_data() == {}

        assert await state2.get_state() == "experiments"
