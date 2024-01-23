from aliceio import F, Router
from aliceio.types import Message, Response

# Для каждого файла мы можем создать отдельный роутер
start_router = Router()


@start_router.message(F.session.new)
async def start_handler(message: Message) -> Response:
    return Response(text="Привет! Внимательно слушаю")
