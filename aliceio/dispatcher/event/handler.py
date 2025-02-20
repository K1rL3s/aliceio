import asyncio
import contextvars
import inspect
import warnings
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Optional

from magic_filter.magic import MagicFilter as OriginalMagicFilter

from aliceio.dispatcher.flags import extract_flags_from_object
from aliceio.filters.base import Filter
from aliceio.handlers import BaseHandler
from aliceio.utils.magic_filter import MagicFilter
from aliceio.utils.warnings import Recommendation

CallbackType = Callable[..., Any]


@dataclass
class CallableObject:
    callback: CallbackType
    awaitable: bool = field(init=False)
    params: set[str] = field(init=False)
    varkw: bool = field(init=False)

    def __post_init__(self) -> None:
        callback = inspect.unwrap(self.callback)
        self.awaitable = inspect.isawaitable(callback) or inspect.iscoroutinefunction(
            callback,
        )
        spec = inspect.getfullargspec(callback)
        self.params = {*spec.args, *spec.kwonlyargs}
        self.varkw = spec.varkw is not None

    def _prepare_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        if self.varkw:
            return kwargs

        return {k: kwargs[k] for k in self.params if k in kwargs}

    async def call(self, *args: Any, **kwargs: Any) -> Any:
        wrapped = partial(self.callback, *args, **self._prepare_kwargs(kwargs))
        if self.awaitable:
            return await wrapped()

        loop = asyncio.get_event_loop()
        context = contextvars.copy_context()
        wrapped = partial(context.run, wrapped)
        return await loop.run_in_executor(None, wrapped)


@dataclass
class FilterObject(CallableObject):
    magic: Optional[MagicFilter] = None

    def __post_init__(self) -> None:
        if isinstance(self.callback, OriginalMagicFilter):
            # MagicFilter instance is callable but generates
            # only "CallOperation" instead of applying the filter
            self.magic = self.callback
            self.callback = self.callback.resolve
            if not isinstance(self.magic, MagicFilter):
                warnings.warn(
                    category=Recommendation,
                    message="You are using F provided by magic_filter "
                    "package directly, but it lacks `.as_()` extension.\n"
                    "Please change the import statement: "
                    "from `from magic_filter import F` "
                    "to `from aliceio import F` to silence this warning.",
                    stacklevel=6,
                )

        super(FilterObject, self).__post_init__()  # noqa: UP008

        if isinstance(self.callback, Filter):
            self.awaitable = True


@dataclass
class HandlerObject(CallableObject):
    filters: Optional[list[FilterObject]] = None
    flags: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        super(HandlerObject, self).__post_init__()  # noqa: UP008
        callback = inspect.unwrap(self.callback)
        if inspect.isclass(callback) and issubclass(callback, BaseHandler):
            self.awaitable = True
        self.flags.update(extract_flags_from_object(callback))

    async def check(self, *args: Any, **kwargs: Any) -> tuple[bool, dict[str, Any]]:
        if not self.filters:
            return True, kwargs
        for event_filter in self.filters:
            check = await event_filter.call(*args, **kwargs)
            if not check:
                return False, kwargs
            if isinstance(check, dict):
                kwargs.update(check)
        return True, kwargs
