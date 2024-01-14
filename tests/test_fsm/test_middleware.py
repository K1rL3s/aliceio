from aliceio.fsm.middleware import FSMContextMiddleware
from aliceio.fsm.storage.memory import MemoryStorage


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
