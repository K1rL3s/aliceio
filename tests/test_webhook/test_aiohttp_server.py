from aiohttp import MultipartReader, web
from aiohttp.test_utils import TestClient
from aiohttp.web_app import Application

from aliceio import Dispatcher, F
from aliceio.methods import Request
from aliceio.types import Message
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
    async def make_reqest(self, client: TestClient, command: str = "test"):
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
                    "command": "закажи пиццу на улицу льва толстого 16 на завтра",
                    "original_utterance": "закажи пиццу на улицу льва толстого, 16 на завтра",  # noqa: E501
                    "markup": {"dangerous_context": True},
                    "payload": {},
                    "nlu": {
                        "tokens": [
                            "закажи",
                            "пиццу",
                            "на",
                            "льва",
                            "толстого",
                            "16",
                            "на",
                            "завтра",
                        ],
                        "entities": [
                            {
                                "tokens": {"start": 2, "end": 6},
                                "type": "YANDEX.GEO",
                                "value": {
                                    "house_number": "16",
                                    "street": "льва толстого",
                                },
                            },
                            {
                                "tokens": {"start": 3, "end": 5},
                                "type": "YANDEX.FIO",
                                "value": {"first_name": "лев", "last_name": "толстой"},
                            },
                            {
                                "tokens": {"start": 5, "end": 6},
                                "type": "YANDEX.NUMBER",
                                "value": 16,
                            },
                            {
                                "tokens": {"start": 6, "end": 8},
                                "type": "YANDEX.DATETIME",
                                "value": {"day": 1, "day_is_relative": True},
                            },
                        ],
                        "intents": {},
                    },
                    "type": "SimpleUtterance",
                },
                "session": {
                    "message_id": 0,
                    "session_id": "42:SESSION_ID",
                    "skill_id": "42:SKILL_ID",
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

    async def test_reply_into_webhook_text(self, skill: MockedSkill, aiohttp_client):
        app = Application()
        dp = Dispatcher()

        @dp.message(F.text == "test")
        def handle_message(msg: Message):
            return msg.answer(text="PASS")

        handler = OneSkillRequestHandler(
            dispatcher=dp,
            skill=skill,
            handle_in_background=False,
        )
        handler.register(app, path="/webhook")
        client: TestClient = await aiohttp_client(app)

        resp = await self.make_reqest(client=client)
        assert resp.status == 200
        assert resp.content_type == "multipart/form-data"
        result = {}
        reader = MultipartReader.from_response(resp)
        while part := await reader.next():
            value = await part.read()
            result[part.name] = value.decode()
        assert result["method"] == "sendMessage"
        assert result["text"] == "PASS"

    async def test_reply_into_webhook_unhandled(
        self,
        skill: MockedSkill,
        aiohttp_client,
    ):
        app = Application()
        dp = Dispatcher()

        @dp.message(F.text == "test")
        def handle_message(msg: Message):
            return msg.answer(text="PASS")

        handler = OneSkillRequestHandler(
            dispatcher=dp,
            skill=skill,
            handle_in_background=False,
        )
        handler.register(app, path="/webhook")
        client: TestClient = await aiohttp_client(app)

        resp = await self.make_reqest(client=client, command="spam")
        assert resp.status == 200
        assert resp.content_type == "multipart/form-data"
        result = {}
        reader = MultipartReader.from_response(resp)
        while part := await reader.next():
            value = await part.read()
            result[part.name] = value.decode()
        assert not result
