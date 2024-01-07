from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, cast

from ...types import AliceObject, Update
from ...types.error_event import ErrorEvent
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
        except (SkipHandler, CancelHandler):  # pragma: no cover
            raise
        except Exception as e:
            response = await self.router.propagate_event(
                update_type="error",
                event=ErrorEvent(alice_request=cast(Update, event), exception=e),
                **data,
            )
            if response is not UNHANDLED:
                return response
            raise
