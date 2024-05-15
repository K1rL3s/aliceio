from typing import Any, Dict

import pytest

from aliceio.fsm.context import FSMContext
from aliceio.fsm.middlewares import FSMApiStorageMiddleware
from aliceio.fsm.storage.base import DEFAULT_DESTINY, StorageKey
from aliceio.fsm.storage.memory import MemoryStorage
from aliceio.fsm.strategy import FSMStrategy
from aliceio.types import AliceResponse, ApiState, Response, Update
from tests.mocked import MockedSkill, create_mocked_update


async def next_handler(*args, **kwargs):
    pass


@pytest.fixture()
def state(skill: MockedSkill) -> FSMContext:
    key = StorageKey(
        skill_id=skill.id,
        user_id="42:USER_ID",
        session_id="42:SESSION_ID",
        application_id="42:APP_ID",
        destiny=DEFAULT_DESTINY,
    )
    return FSMContext(storage=MemoryStorage(), key=key)


# TODO: Тесты на работу FSMApiStorageMiddleware и FSMContextMiddleware в паре
class TestFSMApiStorageMiddleware:
    @pytest.mark.parametrize(
        "strategy,api_state",
        [
            [
                FSMStrategy.USER,
                ApiState(
                    user={"state": FSMStrategy.USER, "data": {"foo": "bar"}},
                    session={},
                    application={},
                ),
            ],
            [
                FSMStrategy.SESSION,
                ApiState(
                    user={},
                    session={"state": FSMStrategy.SESSION, "data": {"foo": "bar"}},
                    application={},
                ),
            ],
            [
                FSMStrategy.APPLICATION,
                ApiState(
                    user={},
                    session={},
                    application={
                        "state": FSMStrategy.APPLICATION,
                        "data": {"foo": "bar"},
                    },
                ),
            ],
            [
                FSMStrategy.USER,
                ApiState(
                    user=None,
                    session={},
                    application={
                        "state": FSMStrategy.USER,
                        "data": {"foo": "bar"},
                    },
                ),
            ],
        ],
    )
    async def test_resolve_state_data(
        self,
        strategy: FSMStrategy,
        api_state: ApiState,
    ):
        middleware = FSMApiStorageMiddleware(strategy=strategy)

        record = middleware.resolve_state_data(api_state)

        assert record.state == strategy
        assert record.data == {"foo": "bar"}

    @pytest.mark.parametrize(
        "strategy,api_state",
        [
            [
                "random",
                ApiState(
                    user={"state": FSMStrategy.USER, "data": {"foo": "bar"}},
                    session={"state": FSMStrategy.SESSION, "data": {"sess": "ion"}},
                    application={
                        "state": FSMStrategy.APPLICATION,
                        "data": {"foo": "bar"},
                    },
                ),
            ],
        ],
    )
    async def test_resolve_state_data_unknown_strategy(
        self,
        strategy: Any,
        api_state: ApiState,
    ):
        middleware = FSMApiStorageMiddleware(strategy=strategy)

        record = middleware.resolve_state_data(api_state)

        assert record.state == FSMStrategy.SESSION
        assert record.data == {"sess": "ion"}

    async def test_resolve_state_none(self):
        middleware = FSMApiStorageMiddleware(strategy=None)

        record = middleware.resolve_state_data(None)

        assert record.state is None
        assert record.data == {}

    async def test_state_from_alice_no_data(self, state: FSMContext, update: Update):
        for strategy in (
            FSMStrategy.USER,
            FSMStrategy.SESSION,
            FSMStrategy.APPLICATION,
        ):
            middleware = FSMApiStorageMiddleware(strategy=strategy)
            await middleware.set_state_from_alice(update, state)
            assert await state.get_state() is None
            assert await state.get_data() == {}

    async def test_state_from_alice_data_and_strategy(self, state: FSMContext):
        update = create_mocked_update(
            user_state={"state": "MyState", "data": {"foo": "bar"}},
        )
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)

        assert await state.get_state() is None
        assert await state.get_data() == {}

        await middleware.set_state_from_alice(update, state)

        assert await state.get_state() == "MyState"
        assert await state.get_data() == {"foo": "bar"}

    @pytest.mark.parametrize(
        "strategy,state_attr,new_state",
        [
            [
                FSMStrategy.USER,
                "user_state_update",
                {"state": "user", "data": {"foo": "bar"}},
            ],
            [
                FSMStrategy.SESSION,
                "session_state",
                {"state": "session", "data": {"foo": "bar"}},
            ],
            [
                FSMStrategy.APPLICATION,
                "application_state",
                {"state": "application", "data": {"foo": "bar"}},
            ],
        ],
    )
    async def test_set_new_state(
        self,
        strategy: FSMStrategy,
        state_attr: str,
        new_state: Dict[str, Any],
    ):
        middleware = FSMApiStorageMiddleware(strategy=strategy)
        response = AliceResponse(response=Response(text="ok"))

        state_attrs = ["user_state_update", "session_state", "application_state"]
        for attr in state_attrs:
            assert getattr(response, attr) is None
        state_attrs.remove(state_attr)

        middleware.set_new_state(response, new_state)

        assert getattr(response, state_attr) == new_state
        for attr in state_attrs:
            assert getattr(response, attr) is None

    @pytest.mark.parametrize(
        "strategy,new_state",
        [
            [
                "unknown",
                {"state": "session", "data": {"foo": "bar"}},
            ],
        ],
    )
    async def test_set_new_state_unknown_strategy(
        self,
        strategy: Any,
        new_state: Dict[str, Any],
        state_attr: str = "session_state",
    ):
        middleware = FSMApiStorageMiddleware(strategy=strategy)
        response = AliceResponse(response=Response(text="ok"))

        state_attrs = ["user_state_update", "session_state", "application_state"]
        for attr in state_attrs:
            assert getattr(response, attr) is None
        state_attrs.remove(state_attr)

        middleware.set_new_state(response, new_state)

        assert getattr(response, state_attr) == new_state
        for attr in state_attrs:
            assert getattr(response, attr) is None

    async def test_set_new_state_with_anonymous_user(self, state: FSMContext):
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)
        response = AliceResponse(response=Response(text="test"))
        new_state = {"state": "session", "data": {"foo": "bar"}}

        state_attrs = ["user_state_update", "session_state", "application_state"]
        for attr in state_attrs:
            assert getattr(response, attr) is None
        state_attrs.remove("application_state")

        middleware.set_new_state(response, new_state, is_anonymous=True)

        assert response.application_state == new_state
        for attr in state_attrs:
            assert getattr(response, attr) is None

    async def test_set_state_to_alice(self, state: FSMContext):
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)
        result = AliceResponse(response=Response(text="test"))
        await state.set_state("MyState")
        await state.set_data({"foo": "bar"})
        await state.update_data(bar="foo")

        assert result.user_state_update is None

        await middleware.set_state_to_alice(result, state)

        assert result.user_state_update == {
            "state": "MyState",
            "data": {"foo": "bar", "bar": "foo"},
        }
        assert await state.get_state() == "MyState"
        assert await state.get_data() == {"foo": "bar", "bar": "foo"}  # нет очистки

    async def test_set_state_to_alice_empty_context(self, state: FSMContext):
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)
        result = AliceResponse(response=Response(text="test"))

        assert result.user_state_update is None
        assert result.session_state is None
        assert result.application_state is None

        await middleware.set_state_to_alice(result, state)

        assert result.user_state_update == {"state": None, "data": {}}
        assert result.session_state is None
        assert result.application_state is None
        assert await state.get_state() is None
        assert await state.get_data() == {}

    async def test_call(self, state: FSMContext):
        async def next_handler(handler, data) -> AliceResponse:
            state = data["state"]
            assert await state.get_state() == "MyState"
            assert await state.get_data() == {"foo": "bar"}

            await state.set_state("AnotherState")
            await state.set_data({"42": "24"})
            await state.update_data(bar="foo")

            return AliceResponse(response=Response(text="test"))

        update = create_mocked_update(
            user_state={"state": "MyState", "data": {"foo": "bar"}},
        )
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)
        data = {"state": state}

        result = await middleware(next_handler, update, data)

        assert result.user_state_update == {
            "state": "AnotherState",
            "data": {"42": "24", "bar": "foo"},
        }
        assert result.session_state is None
        assert result.application_state is None  # есть очистка
        assert data["raw_state"] == "MyState"

    async def test_call_with_none_respone(self, state: FSMContext):
        async def next_handler(handler, data) -> None:
            state = data["state"]
            await state.set_state("AnotherState")
            await state.set_data({"42": "24"})
            await state.update_data(bar="foo")

        update = create_mocked_update(
            user_state={"state": "MyState", "data": {"foo": "bar"}},
        )
        middleware = FSMApiStorageMiddleware(strategy=FSMStrategy.USER)
        data = {"state": state}

        result = await middleware(next_handler, update, data)

        assert result is None
        assert await state.get_state() is None
        assert await state.get_data() == {}  # есть очистка
        assert data["raw_state"] == "MyState"
