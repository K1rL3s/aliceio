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
[![Foss Kruzhok](https://img.shields.io/badge/Foss_2024-%D0%9F%D0%BE%D0%B1%D0%B5%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C-f20067.svg?labelColor=white&style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFyWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4xLWMwMDAgNzkuZWRhMmIzZiwgMjAyMS8xMS8xNC0xMjozMDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjEgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyNC0wNy0wNlQyMDozOToxMyswNTowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNy0wNlQyMDozOToxMyswNTowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjQtMDctMDZUMjA6Mzk6MTMrMDU6MDAiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MTBmZmFmNDctMjdjMi0wYjRlLWJjM2EtZmY0ZGFlZDNhOWI0IiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6MGEzZTYyOGEtNmJkNi01ZTQ3LWJlNmYt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)](https://foss.kruzhok.org/results_2024#creators)

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


### Важно!
Настоятельно рекомендуется иметь опыт работы с [asyncio](https://docs.python.org/3/library/asyncio.html) перед использованием **aliceio**


## Быстрый старт

Как получить `skill_id` и подключить навык к Алисе можно прочитать <a target="_blank" href="https://aliceio.readthedocs.io/ru/latest/tutorial/start/">тут</a>.

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
-   🇷🇺 [\@aliceio_chat](https://t.me/aliceio_chat)


## Лицензия
Copyright © 2023-2024 [K1rL3s](https://github.com/K1rL3s) and [ZloyKobra](https://github.com/ZloyKobra) \
Этот проект использует [MIT](https://github.com/K1rL3s/aliceio/blob/master/LICENSE) лицензию
