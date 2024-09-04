import logging
import os
import sys

from aiohttp import web
from handlers.echo import echo_router
from handlers.ping import ping_router
from handlers.start import start_router

from aliceio import Dispatcher, Skill
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)


def main() -> None:
    dp = Dispatcher()
    # Важно добавить ping_router перед echo_router,
    # иначе эхо будет перехватывать все сообщения и до пинга ничего не дойдёт
    dp.include_routers(start_router, ping_router, echo_router)

    skill_id = os.environ["SKILL_ID"]
    skill = Skill(skill_id=skill_id)

    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
