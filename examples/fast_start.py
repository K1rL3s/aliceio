import os

from aiohttp import web

from aliceio import Dispatcher, Skill
from aliceio.types import Message
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

dp = Dispatcher()
skill = Skill(skill_id=os.environ["SKILL_ID"])


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
