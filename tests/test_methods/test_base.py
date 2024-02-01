from unittest.mock import AsyncMock, patch

import pytest

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import HttpMethod
from aliceio.methods.base import AliceMethod
from tests.mocked import MockedSkill


class MyMethod(AliceMethod[str]):
    __returning__ = str
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer) -> str:
        return "test_url"


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
            mock.assert_awaited_once_with(method)

    async def test_await_without_skill(self, skill: MockedSkill):
        method = MyMethod()
        with pytest.raises(RuntimeError):
            await method

    async def test_skill_call(self, skill: MockedSkill):
        method = MyMethod()
        with patch(
            "aliceio.client.session.base.BaseSession.__call__",
            new_callable=AsyncMock,
        ) as mock:
            await skill(method)
            mock.assert_awaited_once()
            some_skill = mock.await_args_list[0].args[1].skill
            assert skill == some_skill
            assert skill is some_skill
