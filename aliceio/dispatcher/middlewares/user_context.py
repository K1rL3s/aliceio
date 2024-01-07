from typing import Any, Awaitable, Callable, Dict

from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.types import AliceObject, Update


EVENT_FROM_USER_KEY = "event_from_user"
EVENT_SESSION_KEY = "event_session"


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]],
        event: AliceObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            raise RuntimeError("UserContextMiddleware got an unexpected event type!")

        if event.session.user is not None:
            data[EVENT_FROM_USER_KEY] = event.session.user
        data[EVENT_SESSION_KEY] = event.session

        return await handler(event, data)
