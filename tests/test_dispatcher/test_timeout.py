import asyncio

import pytest

from aliceio import Dispatcher, Router
from aliceio.fsm.context import FSMContext
from aliceio.types import TimeoutUpdate, Update
from tests.mocked import MockedSkill


class TestDispatchTimeout:
    async def test_handle_timeout_dp(self, skill: MockedSkill, update: Update):
        dp = Dispatcher(response_timeout=0.1)

        @dp.message()
        async def message_handler(event):
            await asyncio.sleep(1)

        @dp.timeout()
        async def timeout_handler(event, skill, state, event_update) -> str:
            assert isinstance(event, type(update.event))
            assert isinstance(event_update, TimeoutUpdate)
            assert isinstance(skill, MockedSkill)
            assert isinstance(state, FSMContext)
            return "Handled"

        with pytest.warns(RuntimeWarning, match="Detected slow response into webhook"):
            assert await dp.feed_webhook_update(skill, update) == "Handled"

    async def test_handle_timeout_routers(self, skill: MockedSkill, update: Update):
        router = Router()
        dp = Dispatcher(response_timeout=0.1)
        dp.include_router(router)

        @router.message()
        async def message_handler(event):
            await asyncio.sleep(1)

        @router.timeout()
        async def timeout_handler(event, skill, state, event_update) -> str:
            assert isinstance(event, type(update.event))
            assert isinstance(event_update, TimeoutUpdate)
            assert isinstance(skill, MockedSkill)
            assert isinstance(state, FSMContext)
            return "Handled"

        with pytest.warns(RuntimeWarning, match="Detected slow response into webhook"):
            assert await dp.feed_webhook_update(skill, update) == "Handled"
