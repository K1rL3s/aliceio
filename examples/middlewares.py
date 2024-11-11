import logging
import os
import sys
from collections.abc import Awaitable
from typing import Any, Callable

from aiohttp import web

from aliceio import BaseMiddleware, Dispatcher, Router, Skill
from aliceio.types import Message, Response, Update
from aliceio.types.base import AliceObject
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)


class OuterExampleMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: dict[str, Any],
    ) -> Any:
        logging.info(
            "Ивент %s до фильтров (1)",
            update.event.__class__.__name__,
        )
        result = await handler(update, data)
        logging.info(
            "Ивент %s после всей обработки (4)",
            update.event.__class__.__name__,
        )
        return result


class InnerExampleMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: dict[str, Any],
    ) -> Any:
        logging.info(
            "Ивент %s после фильтров и до обработчика (2)",
            update.event.__class__.__name__,
        )
        result = await handler(update, data)
        logging.info(
            "Ивент %s после обработчика (3)",
            update.event.__class__.__name__,
        )
        return result


class MessageMiddleware(BaseMiddleware[Message]):
    def __init__(self, length: int) -> None:
        self.length = length

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: dict[str, Any],
    ) -> Any:
        logging.info("Проверяю сообщение на длину...")

        if len(message.command) < self.length:
            logging.info("Сообщение слишком короткое, блокирую!")
            return Response(text="Ваше сообщение слишком короткое!")

        logging.info("Сообщение достаточное длинное, пропускаю!")
        return await handler(message, data)


class UserAuthorizedMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if event.session.user is None:
            logging.info("Замечен пользователь без аккаунта, блокирую!")
            return Response(
                text="Я вас не знаю, у вас нет аккаунта в Яндексе. "
                "А чтобы пользоваться мной, он нужен!",
            )
        return await handler(event, data)


router = Router()


@router.message()
@router.button_pressed()
@router.purchase()
@router.show_pull()
@router.audio_player()
@router.error()  # Событие фреймворка, не Алисы
@router.timeout()  # Событие фреймворка, не Алисы
async def giga_handler(event: AliceObject) -> Response:
    return Response(text=f"Ой, привет, {event.__class__.__name__}!")


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    # Сначала всегда будут вызываться мидлвари update'а, потом уже ивентов
    dp.update.outer_middleware(OuterExampleMiddleware())
    dp.update.outer_middleware(UserAuthorizedMiddleware())
    dp.update.middleware(InnerExampleMiddleware())

    dp.message.middleware(MessageMiddleware(length=8))

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
