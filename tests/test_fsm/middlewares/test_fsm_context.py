from aliceio.dispatcher.middlewares.user_context import (
    EVENT_FROM_USER_KEY,
    EVENT_SESSION_KEY,
)
from aliceio.fsm.context import FSMContext
from aliceio.fsm.middlewares.fsm_context import (
    FSM_CONTEXT_KEY,
    FSM_STORAGE_KEY,
    RAW_STATE_KEY,
    FSMContextMiddleware,
)
from aliceio.fsm.storage.base import BaseStorage
from aliceio.fsm.storage.memory import MemoryStorage
from aliceio.types import Update
from tests.mocked import MockedSkill


async def next_handler(*args, **kwargs):
    pass


class TestFSMContextMiddleware:
    async def test_close(self):
        flag = False

        class MyStorage(MemoryStorage):
            async def close(self) -> None:
                nonlocal flag
                flag = True

        middleware = FSMContextMiddleware(MyStorage())
        await middleware.close()

        assert flag

    async def test_call(self, update: Update, skill: MockedSkill):
        middleware = FSMContextMiddleware(MemoryStorage())
        data = {
            "skill": MockedSkill,
            EVENT_SESSION_KEY: update.session,
            EVENT_FROM_USER_KEY: update.session.user,
        }

        await middleware(next_handler, update, data)

        assert isinstance(data[FSM_STORAGE_KEY], BaseStorage)
        assert isinstance(data[FSM_CONTEXT_KEY], FSMContext)
        assert data[RAW_STATE_KEY] is None
