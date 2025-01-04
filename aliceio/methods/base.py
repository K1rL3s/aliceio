from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from aliceio.client.context_controller import SkillContextController

from ..client.alice import AliceAPIServer
from ..exceptions import MethodNotMountedToSkillError

if TYPE_CHECKING:
    from ..client.skill import Skill

AliceType = TypeVar("AliceType", bound=Any)


class ApiResponse(BaseModel, Generic[AliceType]):
    result: Optional[AliceType] = None
    status_code: Optional[int] = None


class AliceMethod(SkillContextController, BaseModel, ABC, Generic[AliceType]):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    if TYPE_CHECKING:
        __returning__: ClassVar[type]
        __http_method__: ClassVar[str]
    else:

        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __http_method__(self) -> str:
            pass

    # При emit навык всегда привязывается к навыку,
    # поэтому он всегда будет не None при вызове api_url в AiohttpSession
    @abstractmethod
    def api_url(self, api_server: AliceAPIServer) -> str:
        pass

    async def emit(self, skill: "Skill") -> AliceType:
        return await skill(self)

    def __await__(self) -> Generator[Any, None, AliceType]:
        skill = self._skill
        if not skill:
            raise MethodNotMountedToSkillError
        return self.emit(skill).__await__()
