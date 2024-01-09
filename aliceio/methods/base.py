from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Generator,
    Generic,
    Optional,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict

from aliceio.client.context_controller import SkillContextController

from ..types import InputFile

if TYPE_CHECKING:
    from ..client.skill import Skill

AliceType = TypeVar("AliceType", bound=Any)


# TODO: Сделать под Алису
class Request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: str

    data: Dict[str, Optional[Any]]
    files: Optional[Dict[str, InputFile]]


# TODO: Сделать под Алису
class Response(BaseModel, Generic[AliceType]):
    ok: bool
    result: Optional[AliceType] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None


class AliceMethod(SkillContextController, BaseModel, Generic[AliceType], ABC):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    if TYPE_CHECKING:
        __returning__: ClassVar[type]
        __api_method__: ClassVar[str]
    else:

        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __api_method__(self) -> str:
            pass

    async def emit(self, skill: Skill) -> AliceType:
        return await skill(self)

    def __await__(self) -> Generator[Any, None, AliceType]:
        skill = self._skill
        if not skill:
            raise RuntimeError(
                "This method is not mounted to a any skill instance, "
                "please call it explicilty "
                "with skill instance `await skill(method)`\n"
                "or mount method to a skill instance `method.as_(skill)` "
                "and then call it `await method()`"
            )
        return self.emit(skill).__await__()
