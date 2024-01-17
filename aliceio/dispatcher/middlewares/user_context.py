from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Union

from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.types import Session, TimeoutEvent, Update, User
from aliceio.types.base import AliceObject

EVENT_FROM_USER_KEY = "event_from_user"
EVENT_SESSION_KEY = "event_session"


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]],
        event: AliceObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Update, TimeoutEvent)):
            raise RuntimeError("UserContextMiddleware got an unexpected event type!")

        session, user = self.resolve_event_context(event=event)

        if user is not None:
            data[EVENT_FROM_USER_KEY] = user
        data[EVENT_SESSION_KEY] = session

        return await handler(event, data)

    @classmethod
    def resolve_event_context(
        cls,
        event: Union[Update, TimeoutEvent],
    ) -> Tuple[Session, Optional[User]]:
        return event.session, event.session.user
