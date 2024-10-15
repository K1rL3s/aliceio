from typing import TYPE_CHECKING, Any

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.exceptions import MethodNotMountedToSkillError
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, PreUploadedSound


class UploadSound(AliceMethod[PreUploadedSound]):
    __returning__ = PreUploadedSound
    __http_method__ = HttpMethod.POST

    file: InputFile

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            file: InputFile,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                file=file,
                **__pydantic_kwargs,
            )

    def api_url(self, api_server: AliceAPIServer) -> str:
        if self.skill is None:
            raise MethodNotMountedToSkillError
        return api_server.upload_file_url(
            skill_id=self.skill.id,
            file_type=FileType.SOUNDS,
        )
