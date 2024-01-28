from typing import Any

from magic_filter import AttrDict, MagicFilter

from aliceio.filters.base import Filter
from aliceio.types.alice_event import AliceEvent


class MagicData(Filter):
    """Этот фильтр помогает фильтровать события с контекстными данными."""

    __slots__ = "magic_data"

    def __init__(self, magic_data: MagicFilter) -> None:
        self.magic_data = magic_data

    async def __call__(self, event: AliceEvent, *args: Any, **kwargs: Any) -> Any:
        return self.magic_data.resolve(
            AttrDict({"event": event, **dict(enumerate(args)), **kwargs})
        )

    def __str__(self) -> str:
        return self._signature_to_string(magic_data=self.magic_data)
