from typing import Awaitable, Callable

from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_app import Application

from aliceio import Dispatcher, F
from aliceio.methods import Request
from aliceio.types import AliceResponse, Message, Response
from aliceio.webhook.aiohttp_server import (
    OneSkillRequestHandler,
    ip_filter_middleware,
    setup_application,
)
from aliceio.webhook.security import IPFilter
from tests.mocked.mocked_skill import MockedSkill


class TestAiohttpServer:
    def test_setup_application(self):
        app = Application()

        dp = Dispatcher()
        setup_application(app, dp)

        assert len(app.router.routes()) == 0
        assert len(app.on_startup) == 2
        assert len(app.on_shutdown) == 1

    async def test_middleware(self, aiohttp_client):
        app = Application()
        ip_filter = IPFilter.default()
        app.middlewares.append(ip_filter_middleware(ip_filter))

        async def handler(request: Request):
            return web.json_response({"ok": True})

        app.router.add_route("POST", "/webhook", handler)
        client: TestClient = await aiohttp_client(app)

        resp = await client.post("/webhook")
        assert resp.status == 401

        resp = await client.post(
            "/webhook",
            headers={"X-Forwarded-For": "149.154.167.220"},
        )
        assert resp.status == 200

        resp = await client.post(
            "/webhook",
            headers={"X-Forwarded-For": "149.154.167.220,10.111.0.2"},
        )
        assert resp.status == 200


class TestOneSkillRequestHandler:
    async def make_reqest(
        self,
        client: TestClient,
        command: str = "test",
        skill_id: str = "42:SKILL_ID",
    ):
        return await client.post(
            "/webhook",
            json={
                "meta": {
                    "locale": "ru-RU",
                    "timezone": "Europe/Moscow",
                    "client_id": "yandex.searchplugin/7.16 (none none; android 4.4.2)",
                    "interfaces": {
                        "screen": {},
                        "account_linking": {},
                        "audio_player": {},
                    },
                },
                "request": {
                    "command": command,
                    "original_utterance": command,
                    "markup": {"dangerous_context": True},
                    "payload": {},
                    "type": "SimpleUtterance",
                },
                "session": {
                    "message_id": 0,
                    "session_id": "42:SESSION_ID",
                    "skill_id": skill_id,
                    "user_id": "42:DEPRECATED_USER_ID",
                    "user": {
                        "user_id": "42:USER_ID",
                        "access_token": "42:ACCESS_TOKEN",
                    },
                    "application": {"application_id": "42:APP_TOKEN"},
                    "new": True,
                },
                "state": {
                    "session": {"value": 10},
                    "user": {"value": 42},
                    "application": {"value": 37},
                },
                "version": "1.0",
            },
        )

    async def test_verify_skill_id_in_webhook_request(
        self,
        skill: MockedSkill,
        aiohttp_client: Callable[..., Awaitable[TestClient]],
    ):
        app = Application()
        dp = Dispatcher()

        @dp.message()
        def handle_message(msg: Message) -> AliceResponse:
            return AliceResponse(response=Response(text="test"))

        handler = OneSkillRequestHandler(dispatcher=dp, skill=skill)
        handler.register(app, path="/webhook")
        client: TestClient = await aiohttp_client(app)

        resp = await self.make_reqest(client=client, command="test", skill_id=skill.id)
        assert resp.status == 200
        assert resp.content_type == "application/json"

        resp = await self.make_reqest(client=client, command="test", skill_id="kaboom")
        assert resp.status == 406
        assert resp.content_type == "text/plain"

    async def test_reply_into_webhook_alice_response(
        self,
        skill: MockedSkill,
        aiohttp_client: Callable[..., Awaitable[TestClient]],
    ):
        app = Application()
        dp = Dispatcher()

        @dp.message(F.command == "test")
        def handle_message(msg: Message) -> Response:
            return Response(text="test")

        handler = OneSkillRequestHandler(dispatcher=dp, skill=skill)
        handler.register(app, path="/webhook")
        client = await aiohttp_client(app)

        resp = await self.make_reqest(client=client, command="test")
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == {
            "response": {"text": "test", "end_session": False},
            "version": "1.0",
        }

    async def test_reply_into_webhook_unhandled(
        self,
        skill: MockedSkill,
        aiohttp_client: Callable[..., Awaitable[TestClient]],
    ):
        app = Application()
        dp = Dispatcher()

        @dp.message(F.command == "test")
        def handle_message(msg: Message) -> Response:
            return Response(text="test")

        handler = OneSkillRequestHandler(dispatcher=dp, skill=skill)
        handler.register(app, path="/webhook")
        client = await aiohttp_client(app)

        resp = await self.make_reqest(client=client, command="spam")
        assert resp.status == 404
        assert resp.content_type == "application/json"
        assert await resp.json() is None
