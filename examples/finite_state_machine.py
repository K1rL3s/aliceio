import logging
import os
import sys
from typing import Any, Dict

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.fsm.context import FSMContext
from aliceio.fsm.state import State, StatesGroup
from aliceio.types import Message, Response, TextButton
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

form_router = Router()


class Form(StatesGroup):
    name = State()
    like_skills = State()
    device = State()


@form_router.message(F.session.new)
async def new_session(message: Message, state: FSMContext) -> Response:
    await state.set_state(Form.name)
    return Response(text="Привет! Как тебя зовут?")


@form_router.message(F.command == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> Response:
    """Позволяет пользователю отменить любое действие."""
    current_state = await state.get_state()
    if current_state is not None:
        logging.info("Cancelling state %r", current_state)
        await state.clear()

    return Response(text="Окей, стою. Пока-пока!", end_session=True)


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> Response:
    await state.update_data(name=message.command)
    await state.set_state(Form.like_skills)
    return Response(
        text=f"Рад познакомиться, {message.command}!\nТебе нравятся навыки Алисы?",
        buttons=[
            TextButton(title="Да"),
            TextButton(title="Нет"),
        ],
    )


@form_router.message(Form.like_skills, F.command == "нет")
async def process_dont_like_skills(message: Message, state: FSMContext) -> Response:
    data = await state.get_data()
    await state.clear()
    return Response(
        text="Ну, бывает.\n" + show_summary(data=data, positive=False),
        end_session=True,
    )


@form_router.message(Form.like_skills, F.command == "да")
async def process_like_skills(message: Message, state: FSMContext) -> Response:
    await state.set_state(Form.device)
    return Response(
        text="Класс! Мне тоже!\nЧерез какое устройство ты обычно их используешь?"
    )


@form_router.message(Form.like_skills)
async def process_unknown_write_skills(message: Message) -> Response:
    return Response(
        text="Не могу понять тебя... Можешь повторить, пожалуйста?",
        buttons=[
            TextButton(title="Да"),
            TextButton(title="Нет"),
        ],
    )


@form_router.message(Form.device)
async def process_device(message: Message, state: FSMContext) -> Response:
    data = await state.update_data(device=message.command)
    await state.clear()

    if message.command == "телефон":
        text = "С телефона? Да, это самое удобное, с чего можно пользоваться Алисой.\n"
    else:
        text = ""
    text += show_summary(data=data)

    return Response(text=text, end_session=True)


def show_summary(data: Dict[str, Any], positive: bool = True) -> str:
    name = data["name"]
    device = data.get("device", "чём-то непонятном")
    text = f"Я буду помнить, {name}, что "
    text += (
        f"тебе нравятся навыки Алисы на {device}."
        if positive
        else "тебе не нравятся навыки Алисы..."
    )
    return text


def main() -> None:
    # use_api_storage можно и на False,
    # тогда будет использоваться хранилище на текущей машине
    dp = Dispatcher(use_api_storage=True, response_timeout=10**9)
    dp.include_router(form_router)

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
