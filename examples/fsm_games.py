import os
import random
from typing import Any, Dict, List, Sequence, cast

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.filters import BaseFilter
from aliceio.fsm.context import FSMContext
from aliceio.fsm.state import State, StatesGroup
from aliceio.types import ButtonPressed, Message, Response, TextButton
from aliceio.types.alice_event import AliceEvent
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

CANCEL_STATE_WORDS = ("стоп", "отмен", "прекрати", "выйти", "выход")
GAMES_LIST = ("угадай число", "наперстки")
THIMBLE = "🗑️"


class Game(StatesGroup):
    select = State()
    guess_num = State()
    thimbles = State()


class ContainsFilter(BaseFilter):
    def __init__(self, words: Sequence[str]) -> None:
        self.words = words

    async def __call__(self, message: Message) -> bool:
        return any(word in message.command for word in self.words)


router = Router()


# Начало диалога с навыком и выход из игры
@router.message(F.session.new)
@router.message(ContainsFilter(CANCEL_STATE_WORDS))
async def new_session(message: Message, state: FSMContext) -> Response:
    await state.clear()
    await state.set_state(Game.select)
    return Response(
        text="Привет! Давай играть! Выбери игру:",
        buttons=[TextButton(title=title.capitalize()) for title in GAMES_LIST],
    )


# Пользователь выбрал игру
@router.message(Game.select, ContainsFilter(GAMES_LIST))
async def select_game(message: Message, state: FSMContext) -> Response:
    text = "Отлично! Играем в "
    if "угадай число" in message.text:
        text += "угадайку.\nЯ загадал число от 1 до 100, угадывай!"
        buttons = [TextButton(title=title) for title in ("Сдаюсь", "Прекратить")]
        await state.set_state(Game.guess_num)
        await state.set_data(my_num=random.randint(1, 100))
    else:
        text += "напрёстки.\nКручу, верчу, запутать хочу! Где?"
        buttons = generate_thimbles()
        await state.set_state(Game.thimbles)
    return Response(text=text, buttons=buttons)


# Сработает, когда состояние Game.guess_num и отправлено число
@router.message(Game.guess_num, F.text.cast(int).as_("guess_num"))
async def guess_num_guess(
    message: Message,
    state: FSMContext,
    guess_num: int,
) -> Response:
    data = await state.get_data()
    my_num: int = data["my_num"]

    if my_num == guess_num:
        await state.clear()
        text = "Верно! Ты угадал!"
        buttons = None
    else:
        text = "Нет, но ты близко! Попробуй ещё.\nЗагаданное число "
        if my_num > guess_num:
            text += "больше"
        else:
            text += "меньше"
        buttons = [TextButton(title=title) for title in ("Сдаюсь", "Прекратить")]

    return Response(text=text, buttons=buttons)


# Сработает, когда состояние Game.guess_num и пользователь сдаётся
@router.message(Game.guess_num, F.text.contains("сдаюсь"))
async def guess_num_give_up(message: Message, state: FSMContext) -> str:
    data = await state.get_data()
    my_num: int = data["my_num"]
    await state.clear()
    return f"А ведь ты почти угадал!\nЭто было {my_num}..."


# Сработает при всех остальных случаях с состоянием Game.guess_num
@router.message(Game.guess_num)
async def guess_num_not_digit(message: Message) -> Response:
    return Response(
        text="Это не число, попробуй ещё раз.",
        buttons=[TextButton(title=title) for title in ("Сдаюсь", "Прекратить")],
    )


# Сработает на нажатие кнопки с напёрстком в состоянии Game.thimbles
@router.button_pressed(Game.thimbles)
async def thimbles_button(button: ButtonPressed) -> Response:
    if button.payload["win"]:
        text = "Верно! Ты угадал!"
    else:
        text = "Неа, давай ещё разок."
    text += "\nКручу, верчу! Где?"

    return Response(text=text, buttons=generate_thimbles())


# Сработает на любой текстовый или голосовой ввод в состоянии Game.thimbles
@router.message(Game.thimbles)
async def thimbles_message(message: Message) -> Response:
    return Response(
        text="Попробуй нажать на напёрсток. Если хочешь прекратить, то так и скажи",
        buttons=generate_thimbles(),
    )


# Создаёт три напёрстка, среди которых один выигрышный
def generate_thimbles() -> List[TextButton]:
    buttons = [TextButton(title=THIMBLE, payload={"win": False}) for _ in range(3)]
    cast(Dict[str, Any], random.choice(buttons).payload)["win"] = True
    return buttons


# Обработка всех остальных случаев, которые не обработались выше
@router.message()
@router.button_pressed()
async def wtf_is_happened(event: AliceEvent, state: FSMContext) -> Response:
    await state.clear()
    await state.set_state(Game.select)
    return Response(
        text="Не понял тебя. Давай сначала.",
        buttons=[TextButton(title=title.capitalize()) for title in GAMES_LIST],
    )


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

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
