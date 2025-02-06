<p align="center">
  <a href="https://github.com/K1rl3s/aliceio">
    <img width="200px" height="200px" alt="aliceio" src="https://raw.githubusercontent.com/K1rL3s/aliceio/master/docs/_static/logo-aliceio-trans-text.png">
  </a>
</p>
<h1 align="center">
  AliceIO
</h1>

<div align="center">

[![License](https://img.shields.io/pypi/l/aliceio.svg?style=flat)](https://github.com/K1rL3s/aliceio/blob/master/LICENSE)
[![Status](https://img.shields.io/pypi/status/aliceio.svg?style=flat)](https://pypi.org/project/aliceio/)
[![PyPI](https://img.shields.io/pypi/v/aliceio?label=pypi&style=flat)](https://pypi.org/project/aliceio/)
[![Downloads](https://img.shields.io/pypi/dm/aliceio.svg?style=flat)](https://pypi.org/project/aliceio/)
[![GitHub Repo stars](https://img.shields.io/github/stars/K1rL3s/aliceio?style=flat)](https://github.com/K1rL3s/aliceio/stargazers)
[![Supported python versions](https://img.shields.io/pypi/pyversions/aliceio.svg?style=flat)](https://pypi.org/project/aliceio/)
[![Tests](https://img.shields.io/github/actions/workflow/status/K1rL3s/aliceio/tests.yml?style=flat)](https://github.com/K1rL3s/aliceio/actions)
[![Coverage](https://codecov.io/gh/K1rL3s/aliceio/graph/badge.svg?style=flat)](https://codecov.io/gh/K1rL3s/aliceio)

</div>
<p align="center">
    <b>
        Асинхронный фреймворк для разработки
        <a target="_blank" href="https://dialogs.yandex.ru/store">навыков Алисы</a>
        из
        <a target="_blank" href="https://dialogs.yandex.ru/development">Яндекс.Диалогов</a>
    </b>
</p>
<p align="center">
    Based on <a target="_blank" href="https://github.com/aiogram/aiogram/tree/dev-3.x">aiogram v3</a>
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
- Поддержка [облачных функций Яндекса](https://yandex.cloud/ru/services/functions)


### Важно!
Рекомендуется иметь опыт работы с [asyncio](https://docs.python.org/3/library/asyncio.html) перед использованием **aliceio**


## Быстрый старт

Как получить `skill_id` и подключить навык к Алисе можно прочитать <a target="_blank" href="https://aliceio.readthedocs.io/ru/latest/tutorial/">тут</a>.

### [Yandex Cloud Functions](https://yandex.ru/dev/dialogs/alice/doc/ru/quickstart-programming):
```python
from aliceio import Dispatcher, Skill
from aliceio.types import Message
from aliceio.webhook.yandex_functions import OneSkillYandexFunctionsRequestHandler

dp = Dispatcher()
skill = Skill(skill_id="...")
requests_handler = OneSkillYandexFunctionsRequestHandler(dispatcher=dp, skill=skill)

@dp.message()
async def hello(message: Message) -> str:
    return f"Привет, {message.session.application.application_id}!"

async def main(event, context):
    return await requests_handler(event, context)
```

### Вебхук:
```python
from aiohttp import web
from aliceio import Dispatcher, Skill
from aliceio.types import Message
from aliceio.webhook.aiohttp_server import OneSkillAiohttpRequestHandler, setup_application

dp = Dispatcher()
skill = Skill(skill_id="...")

@dp.message()
async def hello(message: Message) -> str:
    return f"Привет, {message.session.application.application_id}!"

def main() -> None:
    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(dispatcher=dp, skill=skill)

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()
```


## Материалы
- [Туториал](https://aliceio.readthedocs.io/ru/latest/tutorial/)
- [Документация](https://aliceio.readthedocs.io/)
- [Примеры](https://github.com/K1rL3s/aliceio/tree/master/examples)


## Связь
Если у вас есть вопросы, вы можете задать их в Телеграм чате
- 🇷🇺 [\@aliceio_chat](https://t.me/aliceio_chat)


## Лицензия
Copyright © 2023-2025 [K1rL3s](https://github.com/K1rL3s) and [ZloyKobra](https://github.com/ZloyKobra) \
Этот проект использует [MIT](https://github.com/K1rL3s/aliceio/blob/master/LICENSE) лицензию
