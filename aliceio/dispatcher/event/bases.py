from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, NoReturn, Optional, TypeVar, Union
from unittest.mock import sentinel

from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.types.base import AliceObject

MiddlewareEventType = TypeVar("MiddlewareEventType", bound=AliceObject)
NextMiddlewareType = Callable[[MiddlewareEventType, Dict[str, Any]], Awaitable[Any]]
MiddlewareType = Union[
    BaseMiddleware[Any],
    Callable[
        [NextMiddlewareType[MiddlewareEventType], MiddlewareEventType, Dict[str, Any]],
        Awaitable[Any],
    ],
]

UNHANDLED = sentinel.UNHANDLED
REJECTED = sentinel.REJECTED


class SkipHandler(Exception):
    pass


class CancelHandler(Exception):
    pass


def skip(message: Optional[str] = None) -> NoReturn:
    """Вызов исключения :class:`SkipHandler`."""
    raise SkipHandler(message or "Event skipped")
