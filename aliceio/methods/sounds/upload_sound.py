from typing import TYPE_CHECKING, cast

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, PreUploadedSound, UploadedSound

if TYPE_CHECKING:
    from aliceio.client.skill import Skill


class UploadSound(AliceMethod[PreUploadedSound]):
    __returning__ = UploadedSound
    __http_method__ = HttpMethod.POST

    file: InputFile

    def api_url(self, api_server: AliceAPIServer) -> str:
        skill: "Skill" = cast("Skill", self.skill)
        return api_server.upload_file_url(
            skill_id=skill.id,
            file_type=FileType.SOUNDS,
        )
