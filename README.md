<p align="center">
  <a href="https://github.com/K1rl3s/aliceio">
    <img width="200px" height="200px" alt="aliceio" src="https://raw.githubusercontent.com/K1rL3s/aliceio/master/docs/_static/logo_aliceio_trans_text.png">
  </a>
</p>
<h1 align="center">
  AliceIO
</h1>

<p align="center">
  <img alt="License" src="https://img.shields.io/pypi/l/aliceio.svg?style=flat-square">
  <img alt="Status" src="https://img.shields.io/pypi/status/aliceio.svg?style=flat-square">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/aliceio?label=pypi&style=flat-square">
  <img alt="Downloads" src="https://img.shields.io/pypi/dw/aliceio.svg?style=flat-square">
  <img alt="Supported python versions" src="https://img.shields.io/pypi/pyversions/aliceio.svg?style=flat-square">
  <img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/K1rL3s/aliceio/tests.yml?style=flat-square">
</p>
<p align="center">
    <b>
        Асинхронный фреймворк для
        <a href="https://dialogs.yandex.ru/store">навыков Алисы</a>
        из
        <a href="https://dialogs.yandex.ru/development">Яндекс.Диалогов</a>
    </b>
</p>
<p align="center">
    Based on <a href="https://github.com/aiogram/aiogram/tree/dev-3.x">aiogram v3</a>
</p>

## Особенности
- Асинхронность ([asyncio docs](https://docs.python.org/3/library/asyncio.html), [PEP 492](http://www.python.org/dev/peps/pep-0492))
- Тайп-хинты ([PEP 484](http://www.python.org/dev/peps/pep-0484), может быть использован с [mypy](http://mypy-lang.org/))
- Поддержка [PyPy](https://www.pypy.org/)
- Роутеры (Blueprints)
- Машина состояний (Finite State Machine)
- Мидлвари (для входящих событий и вызовов API)
- Мощные [магические фильтры](https://github.com/aiogram/magic-filter)
- Реакция на [долгое время работы](https://yandex.ru/dev/dialogs/alice/doc/publish-settings.html#troubleshooting)


### Важно!
Настоятельно рекомендуется иметь опыт работы с [asyncio](https://docs.python.org/3/library/asyncio.html) перед использование **aliceio**


## [Быстрый старт](https://aliceio.readthedocs.io/ru/latest/tutorial/skill-settings/)

```python
from aiohttp import web
from aliceio import Dispatcher, Skill
from aliceio.types import Message
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

dp = Dispatcher()
skill = Skill(skill_id="...")

@dp.message()
async def hello(message: Message) -> str:
    return f"Привет, {message.session.application.application_id}!"

def main() -> None:
    app = web.Application()
    webhook_requests_handler = OneSkillRequestHandler(dispatcher=dp, skill=skill)

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()
```

## Документация
- [Туториал](https://aliceio.readthedocs.io/ru/latest/tutorial/start/)
- [Документация](https://aliceio.readthedocs.io/)
- [Примеры](https://github.com/K1rL3s/aliceio/tree/master/examples)


## Связь
Если у вас есть вопросы, вы можете посетить чат сообщества в Telegram
-   🇷🇺 [\@aliceio_ru](https://t.me/aliceio_ru)


## Лицензия
Copyright © 2023-2024 [K1rL3s](https://github.com/K1rL3s) and [ZloyKobra](https://github.com/ZloyKobra) \
Этот проект использует [MIT](https://github.com/K1rL3s/aliceio/blob/master/LICENSE) лицензию
