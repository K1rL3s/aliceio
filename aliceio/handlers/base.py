from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from aliceio.types import Update

if TYPE_CHECKING:
    from aliceio import Skill

T = TypeVar("T")


class BaseHandlerMixin(Generic[T]):
    if TYPE_CHECKING:
        event: T
        data: dict[str, Any]


class BaseHandler(BaseHandlerMixin[T], ABC):
    """Базовый класс для всех class-based обработчиков."""

    def __init__(self, event: T, **kwargs: Any) -> None:
        self.event = event
        self.data: dict[str, Any] = kwargs

    @property
    def skill(self) -> "Skill":
        from aliceio import Skill

        if "skill" in self.data:
            return cast(Skill, self.data["skill"])
        raise RuntimeError("Skill instance not found in the context")

    @property
    def update(self) -> Update:
        return cast(Update, self.data.get("update", self.data.get("event_update")))

    @abstractmethod
    async def handle(self) -> Any:  # pragma: no cover
        pass

    def __await__(self) -> Any:
        return self.handle().__await__()
