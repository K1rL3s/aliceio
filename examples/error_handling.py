import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.filters import ExceptionMessageFilter, ExceptionTypeFilter
from aliceio.types import ErrorEvent, Message, Response
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

router = Router()
logger = logging.getLogger(__name__)


class InvalidAge(Exception):
    pass


class InvalidName(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@router.errors(ExceptionTypeFilter(InvalidAge))
async def handle_invalid_age_exception(event: ErrorEvent) -> Response:
    assert isinstance(event.exception, InvalidAge)
    logger.error("Error caught: %r while processing %r", event.exception, event.update)

    assert event.update.message is not None
    assert event.update.event is event.update.message
    return Response(text=f"Произошла ошибка: {repr(event.exception)}")


@router.errors(ExceptionMessageFilter("Invalid"))
async def handle_invalid_exceptions(event: ErrorEvent) -> Response:
    # Так как мы определили `ExceptionTypeFilter` с типом ошибки `InvalidAge` ранее,
    # этот обработчик будет получать ошибки всех типов,
    # если сообщение в ней содержит подстроку "Invalid".
    logger.error(
        "Error `Invalid` caught: %r while processing %r", event.exception, event.update
    )
    return Response(text=f"Произошла ошибка: {repr(event.exception)}")


@router.message(F.command.casefold().startswith("мне"))
async def handle_set_age(message: Message) -> Response:
    age = message.command.replace("мне", "", 1).strip()
    if not age:
        raise InvalidAge('Неверный возраст. Пожалуйста, напиши его как "мне <возраст>"')

    if not age.isdigit():
        raise InvalidAge("Возраст должен быть числом")

    return Response(text=f"Твой возраст через год  - {int(age) + 1}")


@router.message(F.command.casefold().startswith("я"))
async def handle_set_name(message: Message) -> Response:
    name = message.command.replace("я", "", 1).strip()
    if not name:
        raise InvalidName('Invalid name (имя). Пожалуйста, напиши его как "я <имя>"')

    return Response(text=f"Твоё имя - {name}")


@router.message(F.session.new)
async def start_handler(message: Message) -> Response:
    return Response(text="Привет!")


@router.message()
async def help_hanler(message: Message) -> Response:
    return Response(text='Скажите "мне <возраст>" или "я <имя>" :)')


def main() -> None:
    dp = Dispatcher()
    dp.include_routers(router)

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
