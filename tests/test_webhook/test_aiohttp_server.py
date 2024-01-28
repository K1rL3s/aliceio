import json
from typing import Awaitable, Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_app import Application

from aliceio import Dispatcher, F
from aliceio.enums import EventType
from aliceio.types import AliceResponse, Message, Response, Session, Update, User
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

        async def handler(request: web.Request):
            return web.json_response({"ok": True})

        app.router.add_route("POST", "/webhook", handler)
        client: TestClient = await aiohttp_client(app)

        resp = await client.post("/webhook")
        assert resp.status == 401

        resp = await client.post(
            "/webhook",
            headers={"X-Forwarded-For": "178.154.128.1"},
        )
        assert resp.status == 200

        resp = await client.post(
            "/webhook",
            headers={"X-Forwarded-For": "185.32.187.1,10.111.0.2"},
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
                    "session": {"state": "SessionState", "data": {"value": 77}},
                    "user": {},
                    "application": {"state": "AppnState", "data": {"value": 1337}},
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

        resp = await self.make_reqest(client=client, command="test", skill_id=skill.id)
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == {
            "analytics": None,
            "application_state": None,
            "response": {
                "buttons": None,
                "card": None,
                "directives": None,
                "end_session": False,
                "should_listen": None,
                "show_item_meta": None,
                "text": "test",
                "tts": None,
            },
            "session_state": None,
            "user_state_update": None,
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

        resp = await self.make_reqest(client=client, command="spam", skill_id=skill.id)
        assert resp.status == 404
        assert resp.content_type == "application/json"
        assert await resp.json() is None

    @pytest.mark.parametrize(
        "event_type,update,",
        [
            [
                EventType.AUDIO_PLAYER,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "AudioPlayer.PlaybackStarted"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.AUDIO_PLAYER,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "AudioPlayer.PlaybackFinished"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.AUDIO_PLAYER,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "AudioPlayer.PlaybackNearlyFinished"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.AUDIO_PLAYER,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "AudioPlayer.PlaybackStopped"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.AUDIO_PLAYER,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "AudioPlayer.PlaybackFailed", "error": {"message": "fail details", "type": "MEDIA_ERROR_UNKNOWN"}}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.BUTTON_PRESSED,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"nlu": {"tokens": ["надпись", "на", "кнопке"], "entities": [], "intents": {}}, "payload": {}, "type": "ButtonPressed"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.PURCHASE,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "Purchase.Confirmation", "purchase_request_id": "42:REQ_ID", "purchase_token": "42:TOKEN", "order_id": "42:ORDER_ID", "purchase_timestamp": 1600000000, "purchase_payload": {"value": "payload"}, "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...", "signature": "42:SIGN"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.SHOW_PULL,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"type": "Show.Pull", "show_type": "MORNING"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.MESSAGE,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"command": "закажи пиццу на улицу льва толстого 16 на завтра", "original_utterance": "закажи пиццу на улицу льва толстого, 16 на завтра", "markup": {"dangerous_context": true}, "payload": {}, "nlu": {"tokens": ["закажи", "пиццу", "на", "льва", "толстого", "16", "на", "завтра"], "entities": [{"tokens": {"start": 2, "end": 6}, "type": "YANDEX.GEO", "value": {"house_number": "16", "street": "льва толстого"}}, {"tokens": {"start": 3, "end": 5}, "type": "YANDEX.FIO", "value": {"first_name": "лев", "last_name": "толстой"}}, {"tokens": {"start": 5, "end": 6}, "type": "YANDEX.NUMBER", "value": 16}, {"tokens": {"start": 6, "end": 8}, "type": "YANDEX.DATETIME", "value": {"day": 1, "day_is_relative": true}}], "intents": {}}, "type": "SimpleUtterance"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "user": {"value": 42}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
        ],
    )
    async def test_feed_webhook_update(
        self,
        event_type: str,
        update: str,
        skill: MockedSkill,
        aiohttp_client: Callable[..., Awaitable[TestClient]],
    ):
        async def fn_handler(
            event, skill, event_update, event_from_user, event_session
        ):
            assert isinstance(skill, MockedSkill)
            assert isinstance(event_update, Update)
            assert isinstance(event_from_user, User)
            assert isinstance(event_session, Session)
            assert event_update.event == event
            assert event_update.skill is event.skill is skill
            assert event.user == event_from_user
            assert event.session == event_session
            return "Handled"

        app = Application()
        dp = Dispatcher()
        observer = dp.observers[event_type]
        observer.register(fn_handler)

        handler = OneSkillRequestHandler(dispatcher=dp, skill=skill)
        handler.register(app, path="/webhook")
        client = await aiohttp_client(app)
        resp = await client.post("/webhook", data=update)
        assert resp.status == 200
