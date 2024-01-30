from aliceio import F, Router
from aliceio.types import Message, Response

# Для каждого файла мы можем создать отдельный роутер
ping_router = Router()


@ping_router.message(F.command == "ping")
@ping_router.message(F.command == "пинг")
async def echo_handler(message: Message) -> Response:
    return Response(text="понг")
