from typing import Any, Dict
from unittest.mock import AsyncMock, patch

import pytest

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import HttpMethod
from aliceio.methods import AliceType
from aliceio.methods.base import AliceMethod
from tests.mocked import MockedSkill


class MyMethod(AliceMethod[str]):
    __returning__ = str
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return "test_url"

    def response_validate(self, data: Dict[str, Any], **kwargs: Any) -> AliceType:
        return "test_validate"


class TestAliceMethod:
    async def test_emit(self, skill: MockedSkill):
        method = MyMethod()
        with patch(
            "aliceio.client.skill.Skill.__call__",
            new_callable=AsyncMock,
        ) as mock:
            await method.emit(skill)
            mock.assert_called_once_with(method)

    async def test_await(self, skill: MockedSkill):
        method = MyMethod().as_(skill)
        with patch(
            "aliceio.client.skill.Skill.__call__",
            new_callable=AsyncMock,
        ) as mock:
            await method
            mock.assert_called_once_with(method)

    async def test_await_without_skill(self, skill: MockedSkill):
        method = MyMethod()
        with pytest.raises(RuntimeError):
            await method
