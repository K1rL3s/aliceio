import logging
import os
import sys
from typing import List

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.filters import BaseFilter
from aliceio.types import ButtonPressed, Message, Response, TextButton
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

router = Router()


class InWordsFilter(BaseFilter):  # Кастомный фильтр
    def __init__(self, words: List[str]) -> None:
        self.words = words

    async def __call__(self, message: Message) -> bool:
        return message.command in self.words


@router.message(InWordsFilter(["да", "ок", "хорошо"]))
async def yes_message_handler(message: Message) -> str:
    return "Ну да так да, чё бубнеть-то"


# Один и тот же фильтр, но разная запись
@router.button_pressed(F.payload["yes"], F.payload["yes"].is_(True))
async def yes_button_handler(button: ButtonPressed) -> Response:
    return Response(text="Кнопку нажал? Говорить лень?\nНу да так да, чё бубнеть-то")


@router.message(InWordsFilter(["не", "нет", "неа"]))
async def no_message_handler(message: Message) -> str:
    return "Ну на нет и суда нет"


# Один и тот же фильтр, но разная запись
@router.button_pressed(~F.payload["yes"], F.payload["yes"].is_(False))
async def no_button_handler(button: ButtonPressed) -> Response:
    return Response(text="Кнопку нажал? Говорить лень?\nНу на нет и суда нет")


@router.message()
async def any_message_handler(message: Message) -> Response:
    return Response(
        text="Да-да... Да-да...",
        buttons=[
            TextButton(title="Да", payload={"yes": True}),
            TextButton(title="Нет", payload={"yes": False}),
        ],
    )


@router.button_pressed()
async def any_button_handler(message: Message) -> Response:
    return Response(
        text="Да-да... Да-да...",
        buttons=[
            TextButton(title="Да", payload={"yes": True}),
            TextButton(title="Нет", payload={"yes": False}),
        ],
    )


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

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
