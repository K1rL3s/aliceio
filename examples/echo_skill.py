import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, Skill
from aliceio.types import AliceResponse, Message, Response
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

dp = Dispatcher()


@dp.message()
async def echo(message: Message) -> AliceResponse:
    text = "Привет!" if message.session.new else message.original_utterance
    return AliceResponse(response=Response(text=text))


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
