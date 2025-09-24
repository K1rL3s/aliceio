import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from aliceio.dispatcher.dispatcher import Dispatcher
from aliceio.dispatcher.router import Router
from aliceio.fsm.middlewares import FSMApiStorageMiddleware, FSMContextMiddleware
from aliceio.fsm.storage.api import ApiStorage
from aliceio.fsm.storage.memory import MemoryStorage
from aliceio.types import Message, Response, Update
from tests.mocked import MockedSkill


async def simple_message_handler(message: Message):
    await asyncio.sleep(0.2)
    return Response(text="ok")


async def invalid_message_handler(message: Message):
    await asyncio.sleep(0.2)
    raise Exception(42)  # noqa: TRY002


async def anext(ait):
    return await ait.__anext__()


RAW_UPDATE = {
    "meta": {
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}},
    },
    "request": {
        "command": "закажи пиццу на улицу льва толстого 16 на завтра",
        "original_utterance": "закажи пиццу на улицу льва толстого, 16 на завтра",
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
                    "value": {"house_number": "16", "street": "льва толстого"},
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
        "application": {"application_id": "42:APP_ID"},
        "new": True,
    },
    "state": {
        "session": {"state": "SessionState", "data": {"value": 77}},
        "user": {"state": "UserState", "data": {"value": 42}},
        "application": {"state": "ApplicationState", "data": {"value": 1337}},
    },
    "version": "1.0",
}
UPDATE = Update.model_validate(RAW_UPDATE)


# TODO: Полностью покрыть все методы диспетчера
class TestDispatcher:
    def test_init(self):
        dp = Dispatcher()

        assert dp.update.handlers
        assert dp.update.handlers[0].callback == dp._listen_update
        assert dp.update.outer_middleware

    def test_data_bind(self):
        dp = Dispatcher()
        assert dp.get("foo") is None
        assert dp.get("foo", 42) == 42

        dp["foo"] = 1
        assert dp.workflow_data["foo"] == 1
        assert dp["foo"] == 1

        del dp["foo"]
        assert "foo" not in dp.workflow_data

    def test_storage_property(self, dispatcher: Dispatcher):
        assert dispatcher.storage is dispatcher.fsm.storage

    def test_parent_router(self, dispatcher: Dispatcher):
        with pytest.raises(RuntimeError):
            dispatcher.parent_router = Router()
        assert dispatcher.parent_router is None
        dispatcher._parent_router = Router()
        assert dispatcher.parent_router is None

    async def test_feed_raw_update(self, skill: MockedSkill, dispatcher: Dispatcher):
        with patch(
            "aliceio.dispatcher.dispatcher.Dispatcher.feed_update",
            new_callable=AsyncMock,
        ) as mock:
            await dispatcher.feed_raw_update(skill, RAW_UPDATE, data={"k": "v"})
            mock.assert_awaited_once()

            args, kwargs = mock.await_args_list[0]
            assert len(args) == 2
            assert args[0] == skill
            assert isinstance(args[1], Update)
            assert len(kwargs) == 1
            assert kwargs["data"] == {"k": "v"}

    async def test_feed_webhook_update_exception(
        self,
        skill: MockedSkill,
        dispatcher: Dispatcher,
        caplog,
    ):
        dispatcher.message.register(invalid_message_handler)

        with pytest.raises(Exception, match="42"):
            await dispatcher.feed_webhook_update(skill, UPDATE)

        assert "Cause exception while process update" in caplog.text

    async def test_feed_webhook_update_raw(
        self,
        skill: MockedSkill,
        dispatcher: Dispatcher,
    ):
        dispatcher.message.register(simple_message_handler)

        result_1 = await dispatcher.feed_webhook_update(skill, UPDATE)
        result_2 = await dispatcher.feed_webhook_update(skill, RAW_UPDATE)
        assert result_1 == result_2

    async def test_disable_fsm_true(self):
        dp = Dispatcher(disable_fsm=True)

        assert (
            sum(
                isinstance(middleware, FSMContextMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 0
        )
        assert (
            sum(
                isinstance(middleware, FSMApiStorageMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 0
        )

    async def test_disable_fsm_false(self):
        dp = Dispatcher(disable_fsm=False)

        assert (
            sum(
                isinstance(middleware, FSMContextMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 1
        )
        assert (
            sum(
                isinstance(middleware, FSMApiStorageMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 0
        )

    async def test_use_api_storage_true(self):
        dp = Dispatcher(disable_fsm=False, use_api_storage=True)

        assert (
            sum(
                isinstance(middleware, FSMApiStorageMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 1
        )

    async def test_use_api_storage_false(self):
        dp = Dispatcher(disable_fsm=False, use_api_storage=False)

        assert (
            sum(
                isinstance(middleware, FSMApiStorageMiddleware)
                for middleware in dp.update.outer_middleware._middlewares
            )
            == 0
        )

    async def test_init_storage(self):
        class MyStorage(MemoryStorage):
            pass

        dp = Dispatcher()
        my_storage = MyStorage()

        assert (
            dp._create_storage(my_storage, disable_fsm=False, use_api_storage=False)
            == my_storage
        )
        assert (
            dp._create_storage(my_storage, disable_fsm=False, use_api_storage=True)
            == my_storage
        )
        assert (
            dp._create_storage(my_storage, disable_fsm=True, use_api_storage=False)
            == my_storage
        )
        assert (
            dp._create_storage(my_storage, disable_fsm=True, use_api_storage=True)
            == my_storage
        )

        assert isinstance(
            dp._create_storage(None, disable_fsm=False, use_api_storage=False),
            MemoryStorage,
        )
        assert isinstance(
            dp._create_storage(None, disable_fsm=False, use_api_storage=True),
            ApiStorage,
        )
        assert isinstance(
            dp._create_storage(None, disable_fsm=True, use_api_storage=False),
            MemoryStorage,
        )
        assert isinstance(
            dp._create_storage(None, disable_fsm=True, use_api_storage=True),
            MemoryStorage,
        )
