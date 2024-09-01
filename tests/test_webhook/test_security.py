from ipaddress import IPv4Address, IPv4Network
from typing import Set

import pytest

from aliceio.webhook.aiohttp_server.security import IPFilter


class TestSecurity:
    def test_empty_init(self):
        ip_filter = IPFilter()
        assert not ip_filter._allowed_ips

    @pytest.mark.parametrize(
        "ip,result",
        [
            ("127.0.0.1", True),
            ("127.0.0.2", False),
            (IPv4Address("127.0.0.1"), True),
            (IPv4Address("127.0.0.2"), False),
            (IPv4Address("178.154.128.1"), True),
            ("192.168.0.33", False),
            ("10.111.0.5", True),
            ("10.111.0.100", True),
            ("10.111.1.100", False),
        ],
    )
    def test_check_ip(self, ip, result):
        ip_filter = IPFilter(
            ips=[
                "127.0.0.1",
                IPv4Address("178.154.128.1"),
                IPv4Network("10.111.0.0/24"),
            ],
        )
        assert (ip in ip_filter) is result

    def test_default(self):
        ip_filter = IPFilter.default()
        assert isinstance(ip_filter, IPFilter)
        assert len(ip_filter._allowed_ips) == 189668
        assert "5.45.192.1" in ip_filter
        assert "37.9.64.1" in ip_filter
        assert "37.140.128.1" in ip_filter
        assert "77.88.0.1" in ip_filter
        assert "84.252.160.1" in ip_filter
        assert "87.250.224.1" in ip_filter
        assert "90.156.176.1" in ip_filter
        assert "93.158.128.1" in ip_filter
        assert "95.108.128.1" in ip_filter
        assert "141.8.128.1" in ip_filter
        assert "178.154.128.1" in ip_filter
        assert "185.32.187.1" in ip_filter
        assert "213.180.192.1" in ip_filter

    @pytest.mark.parametrize(
        "ip,ip_range",
        [
            ["127.0.0.1", {IPv4Address("127.0.0.1")}],
            ["178.154.128.0/18", set(IPv4Network("178.154.128.0/18").hosts())],
            [IPv4Address("141.8.128.5"), {IPv4Address("141.8.128.5")}],
            [IPv4Network("77.88.0.0/18"), set(IPv4Network("77.88.0.0/18").hosts())],
            [42, set()],
        ],
    )
    def test_allow_ip(self, ip, ip_range: Set[IPv4Address]):
        ip_filter = IPFilter()
        if not ip_range:
            with pytest.raises(ValueError):
                ip_filter.allow_ip(ip)
        else:
            ip_filter.allow_ip(ip)
            assert ip_filter._allowed_ips == ip_range
