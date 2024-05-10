from ipaddress import IPv4Address, IPv4Network
from typing import Optional, Sequence, Set, Union

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
        self._allowed_ips: Set[IPv4Address] = set()

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
