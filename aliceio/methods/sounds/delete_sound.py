from typing import TYPE_CHECKING, Any

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.exceptions import MethodNotMountedToSkillError
from aliceio.methods.base import AliceMethod
from aliceio.types import Result


class DeleteSound(AliceMethod[Result]):
    __returning__ = Result
    __http_method__ = HttpMethod.DELETE

    file_id: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            file_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                file_id=file_id,
                **__pydantic_kwargs,
            )

    def api_url(self, api_server: AliceAPIServer) -> str:
        if self.skill is None:
            raise MethodNotMountedToSkillError
        return api_server.delete_file_url(
            skill_id=self.skill.id,
            file_type=FileType.SOUNDS,
            file_id=self.file_id,
        )
