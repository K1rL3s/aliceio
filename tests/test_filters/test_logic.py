from typing import Any, Union

import pytest

from aliceio.filters import BaseFilter, and_f, invert_f, or_f
from aliceio.filters.logic import _AndFilter, _InvertFilter, _LogicFilter, _OrFilter


class MockedFilter(BaseFilter):
    async def __call__(self, *args: Any) -> bool:
        return True


class TestLogic:
    @pytest.mark.parametrize(
        "obj,case,result",
        [
            [True, and_f(lambda t: t is True, lambda t: t is True), True],
            [True, and_f(lambda t: t is True, lambda t: t is False), False],
            [True, and_f(lambda t: t is False, lambda t: t is False), False],
            [True, and_f(lambda t: {"t": t}, lambda t: t is False), False],
            [True, and_f(lambda t: {"t": t}, lambda t: t is True), {"t": True}],
            [True, or_f(lambda t: t is True, lambda t: t is True), True],
            [True, or_f(lambda t: t is True, lambda t: t is False), True],
            [True, or_f(lambda t: t is False, lambda t: t is False), False],
            [True, or_f(lambda t: t is False, lambda t: t is True), True],
            [True, or_f(lambda t: t is False, lambda t: {"t": t}), {"t": True}],
            [True, or_f(lambda t: {"t": t}, lambda t: {"a": 42}), {"t": True}],
            [True, invert_f(lambda t: t is False), True],
        ],
    )
    async def test_logic(
        self,
        obj: bool,
        case: _LogicFilter,
        result: Union[bool, dict[str, Any]],
    ) -> None:
        assert await case(obj) == result

    @pytest.mark.parametrize(
        "case,type_",
        [
            [or_f(MockedFilter(), MockedFilter()), _OrFilter],
            [and_f(MockedFilter(), MockedFilter()), _AndFilter],
            [invert_f(MockedFilter()), _InvertFilter],
            [~MockedFilter(), _InvertFilter],
        ],
    )
    def test_dunder_methods(self, case: Any, type_: type[_LogicFilter]) -> None:
        assert isinstance(case, type_)
