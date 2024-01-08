import asyncio as _asyncio
from contextlib import suppress

from aliceio.dispatcher.flags import FlagGenerator

from . import enums, methods, types
from .__meta__ import __api_version__, __version__
from .client import session
from .client.skill import Skill
from .dispatcher.dispatcher import Dispatcher
from .dispatcher.middlewares.base import BaseMiddleware
from .dispatcher.router import Router
from .utils.magic_filter import MagicFilter

with suppress(ImportError):
    import uvloop as _uvloop

    _asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())


F = MagicFilter()
flags = FlagGenerator()

__all__ = (
    "__api_version__",
    "__version__",
    "types",
    "methods",
    "enums",
    "Skill",
    "session",
    "Dispatcher",
    "Router",
    "BaseMiddleware",
    "F",
    "flags",
)
