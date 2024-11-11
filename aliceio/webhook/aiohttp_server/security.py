from asyncio import Transport
from collections.abc import Awaitable, Sequence
from ipaddress import IPv4Address, IPv4Network
from typing import Any, Callable, Optional, Union, cast

from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware

from aliceio import loggers

# https://yandex.ru/ips
# https://cloud.yandex.ru/ru/docs/security/ip-list#adresa,-ispolzuemye-yandex-cloud
DEFAULT_YANDEX_NETWORKS = [
    IPv4Network("5.45.192.0/18"),
    IPv4Network("5.255.192.0/18"),
    IPv4Network("37.9.64.0/18"),
    IPv4Network("37.140.128.0/18"),
    IPv4Network("77.88.0.0/18"),
    IPv4Network("84.252.160.0/19"),
    IPv4Network("87.250.224.0/19"),
    IPv4Network("90.156.176.0/22"),
    IPv4Network("93.158.128.0/18"),
    IPv4Network("95.108.128.0/17"),
    IPv4Network("141.8.128.0/18"),
    IPv4Network("178.154.128.0/18"),
    IPv4Network("185.32.187.0/24"),
    IPv4Network("213.180.192.0/19"),
]


class IPFilter:
    def __init__(
        self,
        ips: Optional[Sequence[Union[str, IPv4Network, IPv4Address]]] = None,
    ) -> None:
        self._allowed_ips: set[IPv4Address] = set()

        if ips:
            self.allow(*ips)

    def allow(self, *ips: Union[str, IPv4Network, IPv4Address]) -> None:
        for ip in ips:
            self.allow_ip(ip)

    def allow_ip(self, ip: Union[str, IPv4Network, IPv4Address]) -> None:
        if isinstance(ip, str):
            ip = IPv4Network(ip) if "/" in ip else IPv4Address(ip)
        if isinstance(ip, IPv4Address):
            self._allowed_ips.add(ip)
        elif isinstance(ip, IPv4Network):
            self._allowed_ips.update(ip.hosts())
        else:
            raise ValueError(f"Invalid type of ipaddress: {type(ip)} ('{ip}')")

    @classmethod
    def default(cls) -> "IPFilter":
        return cls(DEFAULT_YANDEX_NETWORKS)

    def check(self, ip: Union[str, IPv4Address]) -> bool:
        if not isinstance(ip, IPv4Address):
            ip = IPv4Address(ip)
        return ip in self._allowed_ips

    def __contains__(self, item: Union[str, IPv4Address]) -> bool:
        return self.check(item)


def ip_filter_middleware(
    ip_filter: IPFilter,
) -> Callable[[web.Request, Handler], Awaitable[Any]]:
    """

    :param ip_filter:
    :return:
    """

    @middleware
    async def _ip_filter_middleware(request: web.Request, handler: Handler) -> Any:
        ip_address, accept = check_ip(ip_filter=ip_filter, request=request)
        if not accept:
            loggers.webhook.warning(
                "Blocking request from an unauthorized IP: %s",
                ip_address,
            )
            raise web.HTTPUnauthorized
        return await handler(request)

    return _ip_filter_middleware


def check_ip(ip_filter: IPFilter, request: web.Request) -> tuple[str, bool]:
    # Попытка вычислить IP-адрес клиента после обратного прокси-сервера.
    if forwarded_for := request.headers.get("X-Forwarded-For", ""):
        # Получаем самый левый IP-адрес, если имеется несколько IP-адресов
        # (запрос получен через несколько прокси/балансировщиков нагрузки)
        forwarded_for, *_ = forwarded_for.split(",", maxsplit=1)
        return forwarded_for, forwarded_for in ip_filter

    # Если обратный прокси-сервер не настроен,
    # IP-адрес можно определить из входящего соединения.
    if peer_name := cast(Transport, request.transport).get_extra_info("peername"):
        host, _ = peer_name
        return host, host in ip_filter

    # Потенциально невозможный случай
    return "", False  # pragma: no cover
