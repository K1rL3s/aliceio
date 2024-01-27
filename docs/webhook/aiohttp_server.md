::: aliceio.webhook.aiohttp_server.setup_application
    handler: python
    options:
      members: true

::: aliceio.webhook.aiohttp_server.check_ip
    handler: python
    options:
      members: true

::: aliceio.webhook.aiohttp_server.ip_filter_middleware
    handler: python
    options:
      members: true

::: aliceio.webhook.aiohttp_server.BaseRequestHandler
    handler: python
    options:
      members:
        - __init__
        - register
        - close
        - resolve_skill
        - handle

::: aliceio.webhook.aiohttp_server.OneSkillRequestHandler
    handler: python
    options:
      members:
        - __init__
        - close
        - resolve_skill
