import asyncio
from typing import Any, AsyncContextManager, AsyncIterable, Dict, List
from unittest.mock import AsyncMock, patch

import aiohttp_socks
import pytest
from aiohttp import ClientError
from aresponses import ResponsesMockServer

from aliceio import Skill
from aliceio.client.alice import AliceAPIServer
from aliceio.client.session import aiohttp
from aliceio.client.session.aiohttp import AiohttpSession
from aliceio.enums import HttpMethod
from aliceio.exceptions import AliceNetworkError, AliceNoCredentialsError
from aliceio.methods import AliceMethod
from aliceio.types import InputFile
from tests.mocked.mocked_skill import MockedSkill


class BareInputFile(InputFile):
    async def read(self):
        yield b""


class TestAiohttpSession:
    async def test_create_session(self):
        session = AiohttpSession()
        assert session._session is None
        aiohttp_session = await session.create_session()
        assert session._session is not None
        assert isinstance(aiohttp_session, aiohttp.ClientSession)
        await session.close()

    async def test_create_proxy_session(self):
        auth = aiohttp.BasicAuth("login", "password", "encoding")
        async with AiohttpSession(proxy=("socks5://proxy.url/", auth)) as session:
            assert session._connector_type == aiohttp_socks.ProxyConnector

            assert isinstance(session._connector_init, dict)
            assert (
                session._connector_init["proxy_type"] is aiohttp_socks.ProxyType.SOCKS5
            )

            aiohttp_session = await session.create_session()
            assert isinstance(aiohttp_session.connector, aiohttp_socks.ProxyConnector)

    async def test_create_proxy_session_proxy_url(self):
        async with AiohttpSession(proxy="socks4://proxy.url/") as session:
            assert isinstance(session.proxy, str)

            assert isinstance(session._connector_init, dict)
            assert (
                session._connector_init["proxy_type"] is aiohttp_socks.ProxyType.SOCKS4
            )

            aiohttp_session = await session.create_session()
            assert isinstance(aiohttp_session.connector, aiohttp_socks.ProxyConnector)

    async def test_create_proxy_session_chained_proxies(self):
        proxy_chain = [
            "socks4://proxy.url/",
            "socks5://proxy.url/",
            "http://user:password@127.0.0.1:3128",
        ]
        async with AiohttpSession(proxy=proxy_chain) as session:
            assert isinstance(session.proxy, list)

            assert isinstance(session._connector_init, dict)

            proxy_infos = session._connector_init["proxy_infos"]
            assert isinstance(proxy_infos, list)
            assert isinstance(proxy_infos[0], aiohttp_socks.ProxyInfo)
            assert proxy_infos[0].proxy_type is aiohttp_socks.ProxyType.SOCKS4
            assert proxy_infos[1].proxy_type is aiohttp_socks.ProxyType.SOCKS5
            assert proxy_infos[2].proxy_type is aiohttp_socks.ProxyType.HTTP

            aiohttp_session = await session.create_session()
            assert isinstance(
                aiohttp_session.connector, aiohttp_socks.ChainProxyConnector
            )

    async def test_reset_connector(self):
        session = AiohttpSession()
        assert session._should_reset_connector
        await session.create_session()
        assert session._should_reset_connector is False
        await session.close()
        assert session._should_reset_connector is False

        assert session.proxy is None
        session.proxy = "socks5://auth:auth@proxy.url/"
        assert session._should_reset_connector
        await session.create_session()
        assert session._should_reset_connector is False

        await session.close()

    async def test_close_session(self):
        session = AiohttpSession()
        await session.create_session()

        with patch("aiohttp.ClientSession.close", new=AsyncMock()) as mocked_close:
            await session.close()
            mocked_close.assert_called_once()

        await session.close()

    def test_build_form_data_with_data_only(self, skill: MockedSkill):
        class TestMethod(AliceMethod[bool]):
            def api_url(self, api_server: AliceAPIServer) -> str:
                return "test"

            __returning__ = bool
            __http_method__ = HttpMethod.POST

            str_: str
            int_: int
            bool_: bool
            null_: None
            list_: List[str]
            dict_: Dict[str, Any]

        session = AiohttpSession()
        form = session.build_form_data(
            skill,
            TestMethod(
                str_="value",
                int_=42,
                bool_=True,
                null_=None,
                list_=["foo"],
                dict_={"bar": "baz"},
            ),
        )

        fields = form._fields
        assert len(fields) == 5
        # assert all(isinstance(field[2], str) for field in fields)
        assert "null_" not in [item[0]["name"] for item in fields]

    def test_build_form_data_with_files(self, skill: Skill):
        class TestMethod(AliceMethod[bool]):
            def api_url(self, api_server: AliceAPIServer) -> str:
                return "http://example.com"

            __returning__ = bool
            __http_method__ = HttpMethod.POST

            key: str
            document: InputFile

        session = AiohttpSession()
        form = session.build_form_data(
            skill,
            TestMethod(key="value", document=BareInputFile()),
        )

        fields = form._fields

        assert len(fields) == 3
        assert fields[1][0]["name"] == "document"
        assert fields[1][2].startswith("attach://")
        assert fields[2][0]["name"] == fields[1][2][9:]
        assert isinstance(fields[2][2], AsyncIterable)

    async def test_make_request(
        self,
        skill: MockedSkill,
        aresponses: ResponsesMockServer,
    ):
        aresponses.add(
            aresponses.ANY,
            "/42:TEST/method",
            "post",
            aresponses.Response(
                status=200,
                text='{"result": 42}',
                headers={"Content-Type": "application/json"},
            ),
        )

        async with AiohttpSession() as session:

            class TestMethod(AliceMethod[int]):
                def api_url(self, api_server: AliceAPIServer) -> str:
                    return "http://localhost/42:TEST/method"

                __returning__ = int
                __http_method__ = HttpMethod.POST

            call = TestMethod()

            result = await session.make_request(skill, call)
            assert isinstance(result, int)
            assert result == 42

    @pytest.mark.parametrize("error", [ClientError("mocked"), asyncio.TimeoutError()])
    async def test_make_request_network_error(self, error):
        async def side_effect(*args, **kwargs):
            raise error

        async with Skill("42:TEST", "42:OUATH").context() as skill:
            with patch(
                "aiohttp.client.ClientSession._request",
                new_callable=AsyncMock,
                side_effect=side_effect,
            ):
                with pytest.raises(AliceNetworkError):
                    await skill.status()

    async def test_context_manager(self):
        async with AiohttpSession() as session:
            assert isinstance(session, AsyncContextManager)

            with patch(
                "aliceio.client.session.aiohttp.AiohttpSession.create_session",
                new_callable=AsyncMock,
            ) as mocked_create_session, patch(
                "aliceio.client.session.aiohttp.AiohttpSession.close",
                new_callable=AsyncMock,
            ) as mocked_close:
                async with session as ctx:
                    assert session == ctx
                mocked_close.assert_awaited_once()
                mocked_create_session.assert_awaited_once()

    async def test_oauth_token_required_for_methods(self):
        skill = Skill("42:TEST")

        with pytest.raises(
            AliceNoCredentialsError,
            match="To use the Alice API, "
            "you need to set an oauth token when creating a Skill",
        ):
            await skill.status()
