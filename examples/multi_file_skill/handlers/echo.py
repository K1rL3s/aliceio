from aliceio import Router
from aliceio.types import Message, Response

# Для каждого файла мы можем создать отдельный роутер
echo_router = Router()


@echo_router.message()
async def echo_handler(message: Message) -> Response:
    return Response(text=message.command)
