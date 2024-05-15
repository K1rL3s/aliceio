from typing import Awaitable, Callable, TypeVar

import pytest

from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.dispatcher.middlewares.response_convert import ResponseConvertMiddleware
from aliceio.types import AliceResponse, Response

T = TypeVar("T")


def create_handler(value: T) -> Callable[..., Awaitable[T]]:
    async def handler(*args, **kwargs) -> T:
        return value

    return handler


class TestResponseConverter:
    async def test_convert_alice_response(self):
        middleware = ResponseConvertMiddleware()

        result = await middleware(
            create_handler(AliceResponse(response=Response(text="test"))),
            None,
            {},
        )
        assert isinstance(result, AliceResponse)
        assert result.response.text == "test"

    async def test_convert_str(self):
        middleware = ResponseConvertMiddleware()

        result = await middleware(create_handler("test"), None, {})
        assert isinstance(result, AliceResponse)
        assert result.response.text == "test"

    async def test_convert_response(self):
        middleware = ResponseConvertMiddleware()

        result = await middleware(create_handler(Response(text="test")), None, {})
        assert isinstance(result, AliceResponse)
        assert result.response.text == "test"

    @pytest.mark.parametrize("value", [None, UNHANDLED, REJECTED])
    async def test_convert_none_unhandled_rejected(self, value):
        middleware = ResponseConvertMiddleware()

        result = await middleware(create_handler(value), None, {})
        assert result is None

    @pytest.mark.parametrize("value", [123, 1.0, [1, 3], {2, 4}, {"a": "b"}])
    async def test_convert_invalid_value(self, value):
        middleware = ResponseConvertMiddleware()

        with pytest.raises(ValueError):
            await middleware(create_handler(value), None, {})
