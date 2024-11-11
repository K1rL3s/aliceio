from collections.abc import Awaitable
from typing import TYPE_CHECKING, Any, Callable

from aliceio.dispatcher.event.bases import UNHANDLED, CancelHandler, SkipHandler
from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.enums import EventType
from aliceio.types import ErrorEvent, Update

if TYPE_CHECKING:
    from aliceio.dispatcher.router import Router


class ErrorsMiddleware(BaseMiddleware[Update]):
    def __init__(self, router: "Router") -> None:
        self.router = router

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except (SkipHandler, CancelHandler):
            raise
        except Exception as e:
            response = await self.router.propagate_event(
                event_type=EventType.ERROR,
                event=ErrorEvent(
                    update=event,
                    exception=e,
                    session=event.session,
                ),
                **data,
            )
            if response is not UNHANDLED:
                return response
            raise
