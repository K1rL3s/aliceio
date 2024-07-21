from typing import TYPE_CHECKING, cast

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import UploadedSoundsList

if TYPE_CHECKING:
    from aliceio.client.skill import Skill


class GetSounds(AliceMethod[UploadedSoundsList]):
    __returning__ = UploadedSoundsList
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer) -> str:
        skill: Skill = cast("Skill", self.skill)
        return api_server.get_all_files_url(
            skill_id=skill.id,
            file_type=FileType.SOUNDS,
        )
