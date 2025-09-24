import asyncio
import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, Router, Skill
from aliceio.exceptions import AliceNoCredentialsError
from aliceio.types import AliceResponse, Message, Response, TimeoutUpdate
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message()
async def echo(message: Message) -> AliceResponse:
    if message.session.new:
        text = "Привет!"
    else:
        text = message.original_utterance
        await asyncio.sleep(5)  # Симуляция долгой работы. 5сек > 4.5сек
    return AliceResponse(response=Response(text=text))


async def on_startup(skill: Skill) -> None:
    try:
        log = str(await skill.status())
    except AliceNoCredentialsError as e:
        log = str(e)
    logger.info("On startup: %s", log)


async def on_shutdown(skill: Skill) -> None:
    try:
        log = str(await skill.status())
    except AliceNoCredentialsError as e:
        log = str(e)
    logger.info("On shutdown: %s", log)


@router.timeout()
async def on_timeout(timeout: TimeoutUpdate) -> AliceResponse:
    return AliceResponse(response=Response(text="Что-то с моим временем не так..."))


def main() -> None:
    dp = Dispatcher(response_timeout=3)  # Для примера 3 секунды, можно и 4 =)
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    skill_id = os.environ["SKILL_ID"]
    oauth_token = os.getenv("OAUTH_TOKEN")  # для `await skill.status()`
    skill = Skill(skill_id=skill_id, oauth_token=oauth_token)

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
