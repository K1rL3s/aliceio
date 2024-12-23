import json
import logging
from collections.abc import Awaitable
from typing import Any, Callable, Optional

import pytest

from aliceio import Dispatcher, F
from aliceio.enums import EventType
from aliceio.types import AliceResponse, Message, Response, Session, Update, User
from aliceio.types.alice_event import AliceEvent
from aliceio.webhook.yandex_functions import (
    OneSkillYandexFunctionsRequestHandler,
    RuntimeContext,
)
from tests.mocked.mocked_skill import MockedSkill


class FakeRuntimeContext(RuntimeContext):
    function_name: str = "function_name"
    function_version: str = "function_version"
    function_folder_id: str = "function_folder_id"
    invoked_function_arn: str = "invoked_function_arn"
    memory_limit_in_mb: int = 128
    request_id: str = "request_id"
    log_group_name: str = "log_group_name"
    log_stream_name: str = "log_stream_name"
    deadline_ms: int = 1000
    token: Optional[str] = None
    aws_request_id: str = "aws_request_id"

    def get_remaining_time_in_millis(self) -> int:
        return self.deadline_ms - 100


class TestYandexFunctionsRequestHandler:
    async def make_request(
        self,
        entrypoint: Callable[
            [dict[str, Any], dict[str, Any]],
            Awaitable[Optional[dict[str, Any]]],
        ],
        command: str = "test",
        skill_id: str = "42:SKILL_ID",
    ):
        event = {
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
        }
        context = {}
        return await entrypoint(event, context)

    async def test_verify_skill_id_in_webhook_request(self, skill: MockedSkill, caplog):
        caplog.set_level(logging.WARNING)

        dp = Dispatcher()

        @dp.message()
        def handle_message(msg: Message) -> AliceResponse:
            return AliceResponse(response=Response(text="test"))

        handler = OneSkillYandexFunctionsRequestHandler(dispatcher=dp, skill=skill)

        resp = await self.make_request(
            entrypoint=handler,
            command="test",
            skill_id=skill.id,
        )
        assert isinstance(resp, dict)
        assert resp["response"]["text"] == "test"

        resp = await self.make_request(
            entrypoint=handler,
            command="test",
            skill_id="kaboom",
        )
        assert resp is None
        assert (
            "Update came from a skill id='kaboom', "
            f"but was expected skill id='{skill.id}'" in caplog.text
        )

    async def test_reply_into_webhook_alice_response(self, skill: MockedSkill):
        dp = Dispatcher()

        @dp.message(F.command == "test")
        def handle_message(msg: Message) -> Response:
            return Response(text="test")

        handler = OneSkillYandexFunctionsRequestHandler(dispatcher=dp, skill=skill)
        resp = await self.make_request(
            entrypoint=handler,
            command="test",
            skill_id=skill.id,
        )
        assert isinstance(resp, dict)
        assert resp == {
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

    async def test_reply_into_webhook_unhandled(self, skill: MockedSkill):
        dp = Dispatcher()

        @dp.message(F.command == "test")
        def handle_message(msg: Message) -> Response:
            return Response(text="test")

        handler = OneSkillYandexFunctionsRequestHandler(dispatcher=dp, skill=skill)

        resp = await self.make_request(
            entrypoint=handler,
            command="spam",
            skill_id=skill.id,
        )
        assert resp is None

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
            [
                # Запрос от анонимного пользователя
                EventType.MESSAGE,
                '{"meta": {"locale": "ru-RU", "timezone": "Europe/Moscow", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "request": {"command": "закажи пиццу на улицу льва толстого 16 на завтра", "original_utterance": "закажи пиццу на улицу льва толстого, 16 на завтра", "markup": {"dangerous_context": true}, "payload": {}, "nlu": {"tokens": ["закажи", "пиццу", "на", "льва", "толстого", "16", "на", "завтра"], "entities": [{"tokens": {"start": 2, "end": 6}, "type": "YANDEX.GEO", "value": {"house_number": "16", "street": "льва толстого"}}, {"tokens": {"start": 3, "end": 5}, "type": "YANDEX.FIO", "value": {"first_name": "лев", "last_name": "толстой"}}, {"tokens": {"start": 5, "end": 6}, "type": "YANDEX.NUMBER", "value": 16}, {"tokens": {"start": 6, "end": 8}, "type": "YANDEX.DATETIME", "value": {"day": 1, "day_is_relative": true}}], "intents": {}}, "type": "SimpleUtterance"}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {"value": 10}, "application": {"value": 37}}, "version": "1.0"}',  # noqa: E501
            ],
            [
                EventType.ACCOUNT_LINKING_COMPLETE,
                '{"meta": {"locale": "ru-RU", "timezone": "Asia/Yekaterinburg", "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)", "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}}}, "session": {"message_id": 0, "session_id": "42:SESSION_ID", "skill_id": "42:SKILL_ID", "user_id": "42:DEPRECATED_USER_ID", "user": {"user_id": "42:USER_ID", "access_token": "42:ACCESS_TOKEN"}, "application": {"application_id": "42:APP_ID"}, "new": false}, "state": {"session": {}, "user": {"data": {}}, "application": {}}, "version": "1.0", "account_linking_complete_event": {}}',  # noqa: E501
            ],
        ],
    )
    async def test_feed_webhook_update(
        self,
        event_type: str,
        update: str,
        skill: MockedSkill,
    ):
        async def fn_handler(
            event,
            skill,
            event_update,
            event_session,
            ycf_context,
            event_from_user=None,
        ):
            assert isinstance(skill, MockedSkill)
            assert isinstance(event_update, Update)
            assert isinstance(event_from_user, User) or event_from_user is None
            assert isinstance(event_session, Session)
            assert event_update.event == event
            assert event_update.skill is event.skill is skill
            if isinstance(event, AliceEvent):
                assert event.user == event_from_user
                assert event.session == event_session
            assert isinstance(ycf_context, FakeRuntimeContext)

            return "Handled"

        dp = Dispatcher()
        observer = dp.observers[event_type]
        observer.register(fn_handler)

        handler = OneSkillYandexFunctionsRequestHandler(dispatcher=dp, skill=skill)
        event = json.loads(update)
        context = FakeRuntimeContext()

        resp = await handler(event=event, context=context)
        assert isinstance(resp, dict)
        assert "response" in resp
