import pytest

from aliceio import Skill
from aliceio.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from aliceio.client.session.middlewares.manager import RequestMiddlewareManager
from aliceio.methods import AliceMethod, Response
from aliceio.types.base import AliceObject


class MyMiddleware(BaseRequestMiddleware):
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType,
        skill: Skill,
        method: AliceMethod[AliceObject],
    ) -> Response[AliceObject]:
        return await make_request(skill, method)


class TestMiddlewareManager:
    async def test_register(self):
        manager = RequestMiddlewareManager()

        @manager
        async def middleware(handler, event, data):
            await handler(event, data)

        assert middleware in manager._middlewares
        manager.unregister(middleware)
        assert middleware not in manager._middlewares

    async def test_wrap_middlewares(self):
        manager = RequestMiddlewareManager()

        manager.register(MyMiddleware())

        @manager()
        @manager
        async def middleware(make_request, skill, method):
            return await make_request(skill, method)

        async def target_call(skill, method, timeout: int = None):
            return timeout

        assert await manager.wrap_middlewares(target_call, timeout=42)(None, None) == 42

    async def test_get_item(self):
        manager = RequestMiddlewareManager()
        m1, m2, m3 = MyMiddleware(), MyMiddleware(), MyMiddleware()

        manager.register(m1)
        manager.register(m2)
        manager.register(m3)

        assert m1 != m2 != m3
        assert manager[0] == m1
        assert manager[1] == m2
        assert manager[2] == m3
        assert manager[:-1] == [m1, m2]
        assert manager[1:] == [m2, m3]

        with pytest.raises(IndexError):
            _ = manager[4]

    async def test_len(self):
        manager = RequestMiddlewareManager()
        m1, m2, m3 = MyMiddleware(), MyMiddleware(), MyMiddleware()

        assert len(manager) == 0
        manager.register(m1)
        assert len(manager) == 1
        manager.register(m2)
        assert len(manager) == 2
        manager.register(m3)
        assert len(manager) == 3
