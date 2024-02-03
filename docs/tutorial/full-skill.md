# Полноценный навык

И теперь нам осталось только написать **серьёзный** многофайловый проект.

Чтобы сделать это, в aliceio можно использовать такой инструмент как `Router`.
Его применение даёт возможность добавлять фильтры и мидлвари для конкретных групп обработчиков и групп роутеров.

## Стандартная иерархия файлов

Для удобства разработки рекомендуется разделять хэндлеры по их функционалу и логике. Например, так:

```text
/src/
├── handlers
│    ├── __init__.py
│    ├── start.py
│    ├── ping.py
│    └── echo.py
├── skill.py
```

### `start.py`

Cоздадим файл `start.py` в папке `handlers`, в котором будет простой хендлер, обрабатывающий начало диалога:

```python
from aliceio import F, Router
from aliceio.types import AliceResponse, Message, Response

start_router = Router()

@start_router.message(F.session.new)  # О фильтрах в следующей главе
async def start_handler(message: Message) -> AliceResponse:
    return AliceResponse(response=Response(text="Привет! Внимательно слушаю"))
```

### `ping.py`

В файле `ping.py` сделаем особый ответ на сообщение с текстом `ping` или `пинг`:

```python
from aliceio import F, Router
from aliceio.types import Message, Response

ping_router = Router()

@ping_router.message(F.command == "ping")
@ping_router.message(F.command == "пинг")
async def echo_handler(message: Message) -> Response:
    return Response(text="понг")
```

### `echo.py`

А в `echo.py` реализуем функционал из прошлой главы, но уже без ветвления:

```python
from aliceio import Router
from aliceio.types import Message

echo_router = Router()

@echo_router.message()
async def echo_handler(message: Message) -> str:
    return message.original_text
```


### `skill.py` (или `main.py`)

Теперь осталось создать файл, в котором мы сделаем бота с диспетчером и зарегистрируем роутеры:

```python
import logging
import sys

from aiohttp import web
from handlers.echo import echo_router
from handlers.ping import ping_router
from handlers.start import start_router

from aliceio import Dispatcher, Skill
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application


def main() -> None:
    dp = Dispatcher()
    # Важно добавить ping_router перед echo_router,
    # иначе эхо будет перехватывать все сообщения и до пинга ничего не дойдёт
    dp.include_routers(start_router, ping_router, echo_router)

    skill = Skill(skill_id="...", oauth_token="...",)

    app = web.Application()
    webhook_requests_handler = OneSkillRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
```

Осталось только связать вместе все мидлвари, фильтры и хэндлеры из предыдущих глав, чтобы создать настоящий навык 😊

## Примеры

* [multi_file_skill](https://github.com/K1rL3s/aliceio/tree/master/examples/multi_file_skill){:target="_blank"}
* [vkbottle](https://vkbottle.readthedocs.io/ru/latest/tutorial/code-separation/){:target="_blank"}
