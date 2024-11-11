from typing import Any

import pytest

from aliceio import Router
from aliceio.dispatcher.event.bases import UNHANDLED, CancelHandler, SkipHandler
from aliceio.dispatcher.middlewares.error import ErrorsMiddleware
from aliceio.exceptions import AliceioError
from aliceio.types import Update
from aliceio.types.base import AliceObject


class TestErrorMiddleware:
    async def test_handler_called_with_event_and_data(self, update: Update):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def handler(event: AliceObject, data: dict[str, Any]) -> str:
            assert event is not None
            assert data is not None
            return "result"

        result = await middleware(handler, update, {})

        assert result == "result"

    async def test_return_handler_result(self, update: Update):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def handler(*_) -> str:
            return "result"

        result = await middleware(handler, update, {})

        assert result == "result"

    @pytest.mark.parametrize(
        "exception",
        [SkipHandler, CancelHandler],
    )
    async def test_re_raise_skip_and_cancel(
        self,
        exception: type[Exception],
        update: Update,
    ):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def raise_exception(*_) -> Any:
            raise exception()

        with pytest.raises(exception):
            await middleware(raise_exception, update, {})

    @pytest.mark.parametrize(
        "exception",
        [SkipHandler, CancelHandler],
    )
    async def test_raise_skip_and_cancel_with_catcher(
        self,
        exception: type[Exception],
        update: Update,
    ):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def raise_exception(*_) -> Any:
            raise exception()

        async def catch_exception(*_):
            return

        router.error.register(catch_exception)

        with pytest.raises(exception):
            await middleware(raise_exception, update, {})

    @pytest.mark.parametrize(
        "exception",
        [AliceioError, ValueError, TypeError, RuntimeError],
    )
    async def test_re_raise_exception(self, exception: type[Exception], update: Update):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def raise_exception(*_):
            raise exception()

        with pytest.raises(exception):
            await middleware(raise_exception, update, {})

    @pytest.mark.parametrize(
        "exception",
        [AliceioError, ValueError, TypeError, RuntimeError],
    )
    async def test_re_raise_exception_with_cathcer(
        self,
        exception: type[Exception],
        update: Update,
    ):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def raise_exception(*_):
            raise exception()

        async def catch_exception(*_):
            return

        router.error.register(catch_exception)

        await middleware(raise_exception, update, {})

    @pytest.mark.parametrize(
        "exception",
        [AliceioError, ValueError, TypeError, RuntimeError],
    )
    async def test_re_raise_exception_with_cathcer_unhandled(
        self,
        exception: type[Exception],
        update: Update,
    ):
        router = Router()
        middleware = ErrorsMiddleware(router)

        async def raise_exception(*_):
            raise exception()

        async def catch_exception(*_):
            return UNHANDLED

        router.error.register(catch_exception)

        with pytest.raises(exception):
            await middleware(raise_exception, update, {})
