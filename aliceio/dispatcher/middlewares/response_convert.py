from collections.abc import Awaitable
from typing import Any, Callable, Optional

from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.types import AliceResponse, Response, Update


class ResponseConvertMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Optional[AliceResponse]:
        result = await handler(event, data)
        return await self.convert_response(result)

    # TODO: Сделать преобразование большего количества типов
    @staticmethod
    async def convert_response(value: Any) -> Optional[AliceResponse]:
        if isinstance(value, AliceResponse):
            return value
        if isinstance(value, Response):
            return AliceResponse(response=value)
        if isinstance(value, str):
            return AliceResponse(response=Response(text=value))
        if value in (None, UNHANDLED, REJECTED):
            return None
        raise ValueError(f"Return type from handlers cannot be `{type(value)}`")
