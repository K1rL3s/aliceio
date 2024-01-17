from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, cast

from ...enums import EventType
from ...types import ErrorEvent, Update
from ...types.base import AliceObject
from ..event.bases import UNHANDLED, CancelHandler, SkipHandler
from .base import BaseMiddleware

if TYPE_CHECKING:
    from ..router import Router


class ErrorsMiddleware(BaseMiddleware):
    def __init__(self, router: Router):
        self.router = router

    async def __call__(
        self,
        handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]],
        event: AliceObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except (SkipHandler, CancelHandler):
            raise
        except Exception as e:
            event = cast(Update, event)
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
