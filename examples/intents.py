"""
Встроенные интенты

https://yandex.ru/dev/dialogs/alice/doc/ru/nlu#predefined-intents
"""

import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, F, Skill
from aliceio.types import Message
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

dp = Dispatcher()


@dp.message(F.nlu.intents["YANDEX.CONFIRM"])
async def confirm(message: Message) -> str:
    return "Тоже согласен, да?"


@dp.message(F.nlu.intents["YANDEX.REJECT"])
async def reject(message: Message) -> str:
    return "Тоже не веришь, не?"


@dp.message(F.nlu.intents["YANDEX.REPEAT"])
async def repeat(message: Message) -> str:
    return "Сейчас повторю, ещё разок?"


@dp.message(F.nlu.intents["YANDEX.HELP"])
async def help(message: Message) -> str:
    return "Тебе помочь, помощь?"


@dp.message()
async def anything_else(message: Message) -> str:
    return "Привет, как дела, пока!"


def main() -> None:
    skill_id = os.environ["SKILL_ID"]
    skill = Skill(skill_id=skill_id)

    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(dispatcher=dp, skill=skill)

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
