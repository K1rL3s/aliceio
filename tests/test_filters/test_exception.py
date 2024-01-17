import re
from typing import NoReturn, Pattern, Union

import pytest

from aliceio import Dispatcher
from aliceio.filters import ExceptionMessageFilter, ExceptionTypeFilter
from aliceio.types import Update
from aliceio.types.alice_event import AliceEvent
from aliceio.types.error_event import ErrorEvent
from tests.mocked import create_mocked_update
from tests.mocked.mocked_skill import MockedSkill


class TestExceptionMessageFilter:
    @pytest.mark.parametrize("value", ["value", re.compile("value")])
    def test_converter(self, value: Union[str, Pattern[str]]) -> None:
        obj = ExceptionMessageFilter(pattern=value)
        assert isinstance(obj.pattern, re.Pattern)

    async def test_match(self, update: Update) -> None:
        f = ExceptionMessageFilter(pattern="BOOM")

        result = await f(
            ErrorEvent(
                update=update,
                exception=Exception(),
                session=update.session,
            )
        )
        assert result is False

        result = await f(
            ErrorEvent(
                update=update,
                exception=Exception("BOOM"),
                session=update.session,
            )
        )
        assert isinstance(result, dict)
        assert "match_exception" in result

    async def test_str(self) -> None:
        f = ExceptionMessageFilter(pattern="BOOM")
        assert str(f) == "ExceptionMessageFilter(pattern=re.compile('BOOM'))"


class MyException(Exception):
    pass


class MyAnotherException(MyException):
    pass


class TestExceptionTypeFilter:
    @pytest.mark.parametrize(
        "exception,value",
        [
            [Exception(), False],
            [ValueError(), False],
            [TypeError(), False],
            [MyException(), True],
            [MyAnotherException(), True],
        ],
    )
    async def test_check(
        self,
        exception: Exception,
        value: bool,
        update: Update,
    ) -> None:
        f = ExceptionTypeFilter(MyException)

        result = await f(
            ErrorEvent(update=update, exception=exception, session=update.session)
        )

        assert result == value

    def test_without_arguments(self) -> None:
        with pytest.raises(ValueError):
            ExceptionTypeFilter()


class TestDispatchException:
    async def test_handle_exception(self, skill: MockedSkill, update: Update) -> None:
        dp = Dispatcher()

        @dp.update()
        async def update_handler(event: AliceEvent) -> NoReturn:
            raise ValueError("BOOM")

        @dp.errors(ExceptionMessageFilter(pattern="BOOM"))
        async def error_handler(error: ErrorEvent) -> str:
            return "Handled"

        with pytest.warns(RuntimeWarning, match="Detected unknown update type"):
            update = create_mocked_update(request_type="42")

            assert await dp.feed_update(skill, update) == "Handled"
