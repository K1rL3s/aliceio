import functools
from typing import Any, Callable, Dict, List, Optional, Sequence, Union, overload

from aliceio.dispatcher.event.bases import (
    MiddlewareEventType,
    MiddlewareType,
    NextMiddlewareType,
)
from aliceio.dispatcher.event.handler import CallbackType
from aliceio.types import AliceObject


class MiddlewareManager(Sequence[MiddlewareType[AliceObject]]):
    def __init__(self) -> None:
        self._middlewares: List[MiddlewareType[AliceObject]] = []

    def register(
        self,
        middleware: MiddlewareType[AliceObject],
    ) -> MiddlewareType[AliceObject]:
        self._middlewares.append(middleware)
        return middleware

    def unregister(self, middleware: MiddlewareType[AliceObject]) -> None:
        self._middlewares.remove(middleware)

    def __call__(
        self,
        middleware: Optional[MiddlewareType[AliceObject]] = None,
    ) -> Union[
        Callable[[MiddlewareType[AliceObject]], MiddlewareType[AliceObject]],
        MiddlewareType[AliceObject],
    ]:
        if middleware is None:
            return self.register
        return self.register(middleware)

    @overload
    def __getitem__(self, item: int) -> MiddlewareType[AliceObject]:
        pass

    @overload
    def __getitem__(self, item: slice) -> Sequence[MiddlewareType[AliceObject]]:
        pass

    def __getitem__(
        self,
        item: Union[int, slice],
    ) -> Union[MiddlewareType[AliceObject], Sequence[MiddlewareType[AliceObject]]]:
        return self._middlewares[item]

    def __len__(self) -> int:
        return len(self._middlewares)

    @staticmethod
    def wrap_middlewares(
        middlewares: Sequence[MiddlewareType[MiddlewareEventType]],
        handler: CallbackType,
    ) -> NextMiddlewareType[MiddlewareEventType]:
        @functools.wraps(handler)
        def handler_wrapper(event: AliceObject, kwargs: Dict[str, Any]) -> Any:
            return handler(event, **kwargs)

        middleware = handler_wrapper
        for m in reversed(middlewares):
            middleware = functools.partial(m, middleware)
        return middleware
