import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, Skill
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)
from examples.oauth.auth_service import authorize_endpoint, token_endpoint
from examples.oauth.skill import router

SKILL_ID = os.environ["SKILL_ID"]
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 80
WEBHOOK_PATH = "/alice"


def main() -> None:
    app = web.Application()

    # Регистрация эндпоинтов авторизации
    app.add_routes([web.get("/authorize", authorize_endpoint)])
    app.add_routes([web.post("/token", token_endpoint)])

    dp = Dispatcher()
    dp.include_router(router)
    skill = Skill(skill_id=SKILL_ID)
    requests_handler = OneSkillAiohttpRequestHandler(dispatcher=dp, skill=skill)

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
