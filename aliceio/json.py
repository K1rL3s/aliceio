from typing import Any, Protocol

from choicelib import choice_in_order  # type: ignore


class JSONModule(Protocol):
    def loads(self, s: str) -> Any:
        ...

    def dumps(self, o: Any) -> str:
        ...

    def load(self, f: str) -> Any:
        ...

    def dump(self, o: Any, f: str) -> None:
        ...


json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"],
    do_import=True,
    default="json",
)
