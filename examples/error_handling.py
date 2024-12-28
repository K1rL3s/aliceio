import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, F, Skill
from aliceio.filters import ExceptionMessageFilter, ExceptionTypeFilter
from aliceio.types import ErrorEvent, Message, Response
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

dp = Dispatcher()
logger = logging.getLogger(__name__)


class InvalidAge(Exception):
    pass


class InvalidName(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dp.errors(ExceptionTypeFilter(InvalidAge))
async def handle_invalid_age_exception(event: ErrorEvent) -> str:
    assert isinstance(event.exception, InvalidAge)
    logger.error("Error caught: %r while processing %r", event.exception, event.update)

    assert event.update.message is not None
    assert event.update.event is event.update.message
    return f"Произошла ошибка: {event.exception!r}"


@dp.errors(ExceptionMessageFilter("Invalid"))
async def handle_invalid_exceptions(event: ErrorEvent) -> str:
    # Так как мы определили `ExceptionTypeFilter` с типом ошибки `InvalidAge` ранее,
    # этот обработчик будет получать ошибки всех типов,
    # если сообщение в ней содержит подстроку "Invalid".
    logger.error(
        "Error `Invalid` caught: %r while processing %r",
        event.exception,
        event.update,
    )
    return f"Произошла ошибка: {event.exception!r}"


@dp.message(F.command.startswith("мне"))
async def handle_set_age(message: Message) -> str:
    age = message.command.replace("мне", "", 1).strip()
    if not age:
        raise InvalidAge('Неверный возраст. Пожалуйста, напиши его как "мне <возраст>"')

    if not age.isdigit():
        raise InvalidAge("Возраст должен быть числом")

    return f"Твой возраст через год  - {int(age) + 1}"


@dp.message(F.command.startswith("я"))
async def handle_set_name(message: Message) -> str:
    name = message.command.replace("я", "", 1).strip()
    if not name:
        raise InvalidName('Invalid name (имя). Пожалуйста, напиши его как "я <имя>"')

    return f"Твоё имя - {name}"


@dp.message(F.session.new)
async def start_handler(message: Message) -> Response:
    return Response(text="Привет!")


@dp.message()
async def help_hanler(message: Message) -> Response:
    return Response(text='Скажите "мне <возраст>" или "я <имя>" :)')


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
