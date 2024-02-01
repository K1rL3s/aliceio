import datetime
import json
from typing import Any, AsyncContextManager, AsyncGenerator, Dict, Optional
from unittest.mock import AsyncMock, patch

import pytest

from aliceio import Skill
from aliceio.client.alice import PRODUCTION, AliceAPIServer
from aliceio.client.session.base import AliceType, BaseSession
from aliceio.exceptions import AliceAPIError, ClientDecodeError
from aliceio.methods import AliceMethod, Status
from aliceio.types import PreQuota, Quota, SpaceStatus
from aliceio.utils.funcs import prepare_value
from tests.mocked.mocked_skill import MockedSkill


class CustomSession(BaseSession):
    async def close(self):
        pass

    async def make_request(
        self,
        token: str,
        method: AliceMethod[AliceType],
        timeout: Optional[int] = None,
    ) -> None:  # type: ignore
        assert isinstance(token, str)
        assert isinstance(method, AliceMethod)

    async def stream_content(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        assert isinstance(url, str)
        assert isinstance(timeout, int)
        assert isinstance(chunk_size, int)
        assert isinstance(raise_for_status, bool)
        yield b"\f" * 10


class TestBaseSession:
    def test_init_api(self):
        session = CustomSession()
        assert session.api == PRODUCTION

    def test_default_props(self):
        session = CustomSession()
        assert session.api == PRODUCTION
        assert session.json_loads == json.loads
        assert session.json_dumps == json.dumps

        def custom_loads(*_):
            return json.loads

        def custom_dumps(*_):
            return json.dumps

        session.json_dumps = custom_dumps
        assert session.json_dumps == custom_dumps
        session.json_loads = custom_loads
        assert session.json_loads == custom_loads

    def test_init_custom_api(self):
        api = AliceAPIServer.from_base("http://example.com")
        session = CustomSession()
        session.api = api
        assert session.api == api
        assert "example.com" in session.api.base

    def test_prepare_value_timedelta(self, skill: MockedSkill):
        value = prepare_value(datetime.timedelta(minutes=2), files={})
        assert isinstance(value, str)

    def test_check_response_json_decode_error(self):
        session = CustomSession()
        skill = MockedSkill()
        method = Status()

        with pytest.raises(ClientDecodeError, match="JSONDecodeError"):
            session.check_response(
                skill=skill,
                method=method,
                status_code=200,
                content="is not a JSON object",
            )

    def test_check_response_validation_error(self):
        session = CustomSession()
        skill = MockedSkill()
        method = Status()

        with pytest.raises(ClientDecodeError, match="ValidationError"):
            session.check_response(
                skill=skill,
                method=method,
                status_code=200,
                content='{"result": "test"}',
            )

    def test_check_error_response(self):
        session = CustomSession()
        skill = MockedSkill()
        method = Status()

        with pytest.raises(AliceAPIError, match="yoooy bro"):
            session.check_response(
                skill=skill,
                method=method,
                status_code=429,
                content='{"message": "yoooy bro"}',
            )

    def test_check_error_response_validation_error(self):
        session = CustomSession()
        skill = MockedSkill()
        method = Status()

        with pytest.raises(ClientDecodeError, match="ValidationError"):
            session.check_response(
                skill=skill,
                method=method,
                status_code=429,
                content='{"key": "value"}',
            )

    async def test_make_request(self):
        session = CustomSession()

        assert await session.make_request("42:TEST", Status()) is None

    async def test_stream_content(self):
        session = CustomSession()
        stream = session.stream_content(
            "https://www.python.org/static/img/python-logo.png",
            headers={},
            timeout=5,
            chunk_size=65536,
            raise_for_status=True,
        )
        assert isinstance(stream, AsyncGenerator)

        async for chunk in stream:
            assert isinstance(chunk, bytes)

    async def test_context_manager(self):
        session = CustomSession()
        assert isinstance(session, AsyncContextManager)

        with patch(
            "tests.test_api.test_client.test_session.test_base_session.CustomSession.close",
            new_callable=AsyncMock,
        ) as mocked_close:
            async with session as ctx:
                assert session == ctx
            mocked_close.assert_awaited_once()

    def test_add_middleware(self):
        async def my_middleware(skill, method, make_request):
            return await make_request(skill, method)

        session = CustomSession()
        assert not session.middleware._middlewares

        session.middleware(my_middleware)
        assert my_middleware in session.middleware
        assert len(session.middleware) == 1

    async def test_use_middleware(self, skill: MockedSkill):
        flag_before = False
        flag_after = False

        @skill.session.middleware
        async def my_middleware(make_request, b, method):
            nonlocal flag_before, flag_after
            flag_before = True
            try:
                assert isinstance(b, Skill)
                assert isinstance(method, AliceMethod)

                return await make_request(b, method)
            finally:
                flag_after = True

        skill.add_result_for(
            Status,
            result=SpaceStatus(
                images=PreQuota(quota=Quota(total=1000, used=100)),
                sounds=PreQuota(quota=Quota(total=2000, used=200)),
            ),
        )
        assert await skill.status()
        assert flag_before
        assert flag_after
