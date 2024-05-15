import pytest
from pytest_lazyfixture import lazy_fixture

from aliceio.fsm.storage.base import DEFAULT_DESTINY, BaseStorage, StorageKey
from tests.mocked import MockedSkill


@pytest.fixture(name="storage_key")
def create_storage_key(skill: MockedSkill) -> StorageKey:
    return StorageKey(
        skill_id=skill.id,
        user_id="42:USER_ID",
        session_id="42:SESSION_ID",
        application_id="42:APP_ID",
        destiny=DEFAULT_DESTINY,
    )


@pytest.mark.parametrize(
    "storage",
    [lazy_fixture("redis_storage"), lazy_fixture("memory_storage")],
)
class TestStorages:
    async def test_set_state(
        self,
        skill: MockedSkill,
        storage: BaseStorage,
        storage_key: StorageKey,
    ) -> None:
        assert await storage.get_state(key=storage_key) is None

        await storage.set_state(key=storage_key, state="state")
        assert await storage.get_state(key=storage_key) == "state"
        await storage.set_state(key=storage_key, state=None)
        assert await storage.get_state(key=storage_key) is None

    async def test_set_data(
        self,
        skill: MockedSkill,
        storage: BaseStorage,
        storage_key: StorageKey,
    ) -> None:
        assert await storage.get_data(key=storage_key) == {}

        await storage.set_data(key=storage_key, data={"foo": "bar"})
        assert await storage.get_data(key=storage_key) == {"foo": "bar"}
        await storage.set_data(key=storage_key, data={})
        assert await storage.get_data(key=storage_key) == {}

    async def test_update_data(
        self,
        skill: MockedSkill,
        storage: BaseStorage,
        storage_key: StorageKey,
    ) -> None:
        assert await storage.get_data(key=storage_key) == {}
        assert await storage.update_data(key=storage_key, data={"foo": "bar"}) == {
            "foo": "bar",
        }
        assert await storage.update_data(key=storage_key, data={"baz": "spam"}) == {
            "foo": "bar",
            "baz": "spam",
        }
        assert await storage.get_data(key=storage_key) == {
            "foo": "bar",
            "baz": "spam",
        }
