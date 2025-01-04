"""
Пример запуска навыка с командой и без

https://yandex.ru/dev/dialogs/alice/doc/ru/activation#activate
"""

import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, F, Skill
from aliceio.types import Message, Response
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

dp = Dispatcher()


@dp.message(F.session.new, F.command)
async def start_with_command(message: Message) -> str:
    return f'Привет! Это был запуск c командой: "{message.command}"'


@dp.message(F.session.new, F.command == "")  # noqa: PLC1901
async def start_without_command(message: Message) -> str:
    return "Привет! Это был запуск без команды"


@dp.message()
async def other(message: Message) -> Response:
    return Response(text="Перезапуск =)", end_session=True)


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
