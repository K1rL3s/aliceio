import logging
import os
import random
import sys
from typing import Any, Awaitable, Callable, Dict, Union

from aiohttp import web

from aliceio import BaseMiddleware, Dispatcher, F, Router, Skill
from aliceio.filters import BaseFilter
from aliceio.types import Message, User
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

router = Router(name=__name__)


class RandomFloatMiddleware(BaseMiddleware[Message]):
    def __init__(self, start: float = 0.01, end: float = 100.0) -> None:
        self.start = start
        self.end = end

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Добаляем значение в контекст3
        data["float_num"] = round(random.uniform(self.start, self.end), 3)
        return await handler(event, data)


class RandomNumberFilter(BaseFilter):
    async def __call__(
        self,
        message: Message,
        event_from_user: User,
        # Фильтры также могут принимать данные из контекста как обработчики
    ) -> Union[bool, Dict[str, Any]]:
        if message.command == "число":
            # Возврат словаря обновит контекст
            return {"int_num": random.randint(1_000, 10_000)}
        return False


@router.message(RandomNumberFilter())
async def random_number_handler(
    message: Message,
    int_num: int,  # После фильтра можно принять "int_num" как именованный аргумент
    float_num: float,  # А после мидлваря можно принять "float_num"
) -> str:
    return f"🎲 Моё число... {int_num}!\n🤓Шанс на это был ~{float_num}%"


@router.message(F.text.as_("real_text"))
async def start_handler(
    message: Message,
    yoy_num: int,  # Аргумент из даты диспетчера
    kek_num: int,  # Аргумент из даты RequestHandler'а
    real_text: str,  # Аргумент из магического фильтра
) -> str:
    assert real_text == message.text
    return (
        '💻 Скажи "число", и я скажу число, которое я задумал\n'
        f"(точно не {yoy_num} и не {kek_num})"
    )


def main() -> None:
    dp = Dispatcher(yoy_num=42)  # Тоже расширение контекста
    dp.include_router(router)
    dp.message.middleware(RandomFloatMiddleware())

    skill_id = os.environ["SKILL_ID"]
    skill = Skill(skill_id=skill_id)

    app = web.Application()
    webhook_requests_handler = OneSkillRequestHandler(
        dispatcher=dp,
        skill=skill,
        kek_num=1337,  # Тоже расширение контекста
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
