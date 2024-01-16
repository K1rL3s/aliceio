import asyncio
from functools import wraps
from typing import Any

import pytest

from aliceio import Skill
from aliceio.dispatcher.event.handler import HandlerObject
from aliceio.enums import RequestType
from aliceio.handlers import BaseHandler
from aliceio.types import AliceRequest, Update
from tests.mocked import create_mocked_update


class MyHandler(BaseHandler):
    async def handle(self) -> Any:
        await asyncio.sleep(0.1)
        return 42


class TestBaseClassBasedHandler:
    async def test_base_handler(self, update: Update):
        handler = MyHandler(event=update, key=42)

        assert handler.event == update
        assert handler.data["key"] == 42
        assert not hasattr(handler, "filters")
        assert await handler == 42

    async def test_skill_from_context(self, update: Update):
        skill = Skill("42:TEST")
        handler = MyHandler(event=update, key=42, skill=skill)
        assert handler.skill == skill

    async def test_skill_from_context_missing(self, update: Update):
        handler = MyHandler(event=update, key=42)

        with pytest.raises(RuntimeError):
            handler.skill

    async def test_skill_from_data(self, update: Update):
        skill = Skill("42:TEST")
        handler = MyHandler(event=update, key=42, skill=skill)

        assert "skill" in handler.data
        assert handler.skill == skill

    def test_update_from_data(self):
        request = AliceRequest(
            type=RequestType.SIMPLE_UTTERANCE,
            command="test",
            original_utterance="test",
        )
        update = create_mocked_update(request=request)
        handler = MyHandler(event=update.event, update=update)

        assert handler.event == update.event
        assert handler.update == update

    async def test_wrapped_handler(self):
        # wrap the handler on dummy function
        handler = wraps(MyHandler)(lambda: None)
        assert HandlerObject(handler).awaitable is True
