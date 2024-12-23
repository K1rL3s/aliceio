from typing import Any

from aliceio import Dispatcher, Skill
from aliceio.types import AliceResponse, Message, Response
from aliceio.webhook.yandex_functions import (
    OneSkillYandexFunctionsRequestHandler,
    RuntimeContext,
)

dp = Dispatcher()
skill = Skill(skill_id="...")  # Вставьте айди навыка
requests_handler = OneSkillYandexFunctionsRequestHandler(dp, skill)


@dp.message()
async def message_handler(
    message: Message,
    ycf_context: RuntimeContext,
) -> AliceResponse:
    text = "Привет!" if message.session.new else message.original_utterance
    text += (
        "\n\nПеред отправкой у меня осталось "
        f"{ycf_context.get_remaining_time_in_millis()} миллисекунд"
    )
    return AliceResponse(response=Response(text=text))


# Нужно поставить эту функцию как точку входа
async def main(event: dict[str, Any], context: RuntimeContext) -> Any:
    return await requests_handler(event, context)
    # аналогично:
    # return await requests_handler.handle(event, context)
