import logging
import os
import ssl
import sys

from aiohttp import web

from aliceio import Dispatcher, Router, Skill
from aliceio.types import AliceResponse, Message, Response
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

router = Router()


@router.message()
async def echo(message: Message) -> AliceResponse:
    if message.session.new:
        text = "Привет!"
    else:
        text = message.original_utterance
    return AliceResponse(response=Response(text=text))


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    skill_id = os.environ["SKILL_ID"]
    skill = Skill(skill_id=skill_id)

    app = web.Application()
    webhook_requests_handler = OneSkillRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"
    WEBHOOK_SSL_CERT = "/path/to/cert.pem"
    WEBHOOK_SSL_PRIV = "/path/to/private.key"

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, ssl_context=context)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
