from collections.abc import Awaitable
from typing import Any, Callable, Optional

from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.types import Session, Update, User

EVENT_FROM_USER_KEY = "event_from_user"
EVENT_SESSION_KEY = "event_session"
EVENT_UPDATE_KEY = "event_update"


class UserContextMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            raise RuntimeError("UserContextMiddleware got an unexpected event type!")

        session, user = self.resolve_event_context(event=event)

        if user is not None:
            data[EVENT_FROM_USER_KEY] = user
        data[EVENT_SESSION_KEY] = session
        data[EVENT_UPDATE_KEY] = event

        return await handler(event, data)

    @classmethod
    def resolve_event_context(
        cls,
        event: Update,
    ) -> tuple[Session, Optional[User]]:
        return event.session, event.session.user
