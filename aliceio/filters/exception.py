import re
from typing import Any, Dict, Pattern, Type, Union, cast

from aliceio.filters.base import Filter
from aliceio.types.base import AliceObject
from aliceio.types.error_event import ErrorEvent


class ExceptionTypeFilter(Filter):
    """Позволяет определять исключения по типу."""

    __slots__ = ("exceptions",)

    def __init__(self, *exceptions: Type[Exception]):
        """
        :param exceptions: Типы исключений, на которые должен реагировать фильтр.
        """
        if not exceptions:
            raise ValueError("At least one exception type is required")
        self.exceptions = exceptions

    async def __call__(self, obj: AliceObject) -> Union[bool, Dict[str, Any]]:
        return isinstance(cast(ErrorEvent, obj).exception, self.exceptions)


class ExceptionMessageFilter(Filter):
    """Позволяет определять исключения по сообщению в них."""

    __slots__ = ("pattern",)

    def __init__(self, pattern: Union[str, Pattern[str]]) -> None:
        """
        :param pattern: Regexp.
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern

    def __str__(self) -> str:
        return self._signature_to_string(pattern=self.pattern)

    async def __call__(
        self,
        obj: AliceObject,
    ) -> Union[bool, Dict[str, Any]]:
        result = self.pattern.match(str(cast(ErrorEvent, obj).exception))
        if not result:
            return False
        return {"match_exception": result}
