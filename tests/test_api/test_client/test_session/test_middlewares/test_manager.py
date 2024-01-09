from aliceio import Skill
from aliceio.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from aliceio.client.session.middlewares.manager import RequestMiddlewareManager
from aliceio.methods import AliceMethod, Response
from aliceio.types.base import AliceObject


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

        class MyMiddleware(BaseRequestMiddleware):
            async def __call__(
                self,
                make_request: NextRequestMiddlewareType,
                skill: Skill,
                method: AliceMethod[AliceObject],
            ) -> Response[AliceObject]:
                return await make_request(skill, method)

        manager.register(MyMiddleware())

        @manager()
        @manager
        async def middleware(make_request, skill, method):
            return await make_request(skill, method)

        async def target_call(skill, method, timeout: int = None):
            return timeout

        assert await manager.wrap_middlewares(target_call, timeout=42)(None, None) == 42
