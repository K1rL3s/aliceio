from __future__ import annotations

import asyncio
import ssl
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import certifi
from aiohttp import BasicAuth, ClientError, ClientSession, FormData, TCPConnector
from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE

from aliceio.__meta__ import __version__
from aliceio.methods import AliceMethod

from ...exceptions import AliceNetworkError

# from ...exceptions import AliceNetworkError
from ...methods.base import AliceType
from ...types import InputFile
from .base import BaseSession

if TYPE_CHECKING:
    from ..skill import Skill

_ProxyBasic = Union[str, Tuple[str, BasicAuth]]
_ProxyChain = Iterable[_ProxyBasic]
_ProxyType = Union[_ProxyChain, _ProxyBasic]


def _retrieve_basic(basic: _ProxyBasic) -> Dict[str, Any]:
    from aiohttp_socks.utils import parse_proxy_url  # type: ignore

    proxy_auth: Optional[BasicAuth] = None

    if isinstance(basic, str):
        proxy_url = basic
    else:
        proxy_url, proxy_auth = basic

    proxy_type, host, port, username, password = parse_proxy_url(proxy_url)
    if isinstance(proxy_auth, BasicAuth):
        username = proxy_auth.login
        password = proxy_auth.password

    return {
        "proxy_type": proxy_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "rdns": True,
    }


def _prepare_connector(
    chain_or_plain: _ProxyType,
) -> Tuple[Type["TCPConnector"], Dict[str, Any]]:
    from aiohttp_socks import (  # type: ignore
        ChainProxyConnector,
        ProxyConnector,
        ProxyInfo,
    )

    # поскольку кортеж является Iterable(совместим с _ProxyChains),
    # мы предполагаем, что пользователю нужны цепочки прокси,
    # если кортеж представляет собой пару строки(url) и BasicAuth
    if isinstance(chain_or_plain, str) or (
        isinstance(chain_or_plain, tuple) and len(chain_or_plain) == 2
    ):
        chain_or_plain = cast(_ProxyBasic, chain_or_plain)
        return ProxyConnector, _retrieve_basic(chain_or_plain)

    chain_or_plain = cast(_ProxyChain, chain_or_plain)
    infos: List[ProxyInfo] = []
    for basic in chain_or_plain:
        infos.append(ProxyInfo(**_retrieve_basic(basic)))

    return ChainProxyConnector, {"proxy_infos": infos}


class AiohttpSession(BaseSession):
    def __init__(self, proxy: Optional[_ProxyType] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._session: Optional[ClientSession] = None
        self._connector_type: Type[TCPConnector] = TCPConnector
        self._connector_init: Dict[str, Any] = {
            "ssl": ssl.create_default_context(cafile=certifi.where()),
        }
        self._should_reset_connector = True  # флаг определяет состояние коннектора
        self._proxy: Optional[_ProxyType] = None

        if proxy is not None:
            try:
                self._setup_proxy_connector(proxy)
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "In order to use aiohttp client for proxy requests, install "
                    "https://pypi.org/project/aiohttp-socks/"
                ) from exc

    def _setup_proxy_connector(self, proxy: _ProxyType) -> None:
        self._connector_type, self._connector_init = _prepare_connector(proxy)
        self._proxy = proxy

    @property
    def proxy(self) -> Optional[_ProxyType]:
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: _ProxyType) -> None:
        self._setup_proxy_connector(proxy)
        self._should_reset_connector = True

    async def create_session(self) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=self._connector_type(**self._connector_init),
                headers={
                    USER_AGENT: f"{SERVER_SOFTWARE} aliceio/{__version__}",
                },
            )
            self._should_reset_connector = False

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

            # Ждём 250 мс, пока SSL-соединения закроются.
            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            await asyncio.sleep(0.25)

    def build_form_data(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
    ) -> FormData:
        form = FormData(quote_fields=False)
        files: Dict[str, InputFile] = {}
        for key, value in method.model_dump(warnings=False).items():
            value = self.prepare_value(value, skill=skill, files=files)
            if not value:
                continue
            form.add_field(key, value)
        for key, value in files.items():
            form.add_field(
                key,
                value.read(skill),
                filename=value.filename or key,
            )
        return form

    # TODO: Сделать под Алису
    async def make_request(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
        timeout: Optional[int] = None,
    ) -> AliceType:
        session = await self.create_session()

        url = self.api.api_url(method=method.__api_method__)
        form = self.build_form_data(skill=skill, method=method)

        try:
            async with session.post(
                url,
                data=form,
                timeout=self.timeout if timeout is None else timeout,
            ) as resp:
                raw_result = await resp.text()
        except asyncio.TimeoutError:
            raise AliceNetworkError(method=method, message="AliceRequest timeout error")
        except ClientError as e:
            raise AliceNetworkError(
                method=method,
                message=f"{type(e).__name__}: {e}",
            )
        response = self.check_response(
            skill=skill,
            method=method,
            status_code=resp.status,
            content=raw_result,
        )
        return cast(AliceType, response.result)

    async def stream_content(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        if headers is None:
            headers = {}

        session = await self.create_session()

        async with session.get(
            url,
            timeout=timeout,
            headers=headers,
            raise_for_status=raise_for_status,
        ) as resp:
            async for chunk in resp.content.iter_chunked(chunk_size):
                yield chunk

    async def __aenter__(self) -> AiohttpSession:
        await self.create_session()
        return self