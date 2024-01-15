from typing import TYPE_CHECKING, cast

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import Result

if TYPE_CHECKING:
    from aliceio.client.skill import Skill


class DeleteSound(AliceMethod[Result]):
    __returning__ = Result
    __http_method__ = HttpMethod.DELETE

    file_id: str

    def api_url(self, api_server: AliceAPIServer) -> str:
        skill: "Skill" = cast("Skill", self.skill)
        return api_server.delete_file_url(
            skill_id=skill.id,
            file_type=FileType.SOUNDS,
            file_id=self.file_id,
        )
