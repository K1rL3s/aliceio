import logging
import os
import sys

from aiohttp import web
from handlers.echo import echo_router
from handlers.start import start_router

from aliceio import Dispatcher, Skill
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application


def main() -> None:
    dp = Dispatcher()
    dp.include_routers(start_router, echo_router)

    skill_id = os.environ["SKILL_ID"]
    oauth_token = os.getenv("OAUTH_TOKEN")
    skill = Skill(
        skill_id=skill_id,
        oauth_token=oauth_token,
    )

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
