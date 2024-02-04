[IP-адреса Яндекса](https://yandex.ru/ips){:target="_blank"}
```python
from ipaddress import IPv4Network

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
    # IPv6Network("2a02:6b8::/29"),  # ? :(
]
```


::: aliceio.webhook.security.IPFilter
    handler: python
    options:
      members:
        - __init__
        - default
        - allow
        - allow_ip
        - check
        - __contains__
