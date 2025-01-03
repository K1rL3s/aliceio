import logging
import os
import sys

from aiohttp import web

from aliceio import Dispatcher, F, Skill
from aliceio.filters import BaseFilter
from aliceio.fsm.context import FSMContext
from aliceio.fsm.state import State, StatesGroup
from aliceio.types import Message, Response, TextButton
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

dp = Dispatcher()

words_yes = ["да", "давай", "ок", "покупаю", "ладно", "купить"]
all_words = [*words_yes, "нет", "не хочу", "не буду", "отстань"]
site_url = "https://market.yandex.ru/search?text=слон"


class Form(StatesGroup):
    buying = State()


class ContainsFilter(BaseFilter):  # Кастомный фильтр
    def __init__(self, words: list[str]) -> None:
        self.words = words

    async def __call__(self, message: Message) -> bool:
        return any(word in message.command for word in self.words)


@dp.message(F.session.new)
async def new_session(message: Message, state: FSMContext) -> Response:
    await state.set_data(all_words=all_words.copy())
    await state.set_state(Form.buying)

    return Response(
        text="Привет! Купи слона!",
        buttons=[TextButton(title=title.capitalize()) for title in all_words],
    )


@dp.message(Form.buying, ContainsFilter(words_yes))
async def confirm_purchase(message: Message, state: FSMContext) -> Response:
    await state.clear()
    return Response(
        text=f"Круто! Слона можно найти на Яндекс.Маркете!\n{site_url}",
        end_session=True,
    )


@dp.message(Form.buying)
async def next_try(message: Message, state: FSMContext) -> Response:
    data = await state.get_data()
    if message.command in data["all_words"]:
        data["all_words"].remove(message.command)
        await state.update_data(all_words=data["all_words"].copy())

    return Response(
        text=f"Все говорят {message.command}, а ты купи слона!",
        buttons=[TextButton(title=title.capitalize()) for title in data["all_words"]],
    )


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
