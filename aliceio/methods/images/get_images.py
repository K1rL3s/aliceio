from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.exceptions import MethodNotMountedToSkillError
from aliceio.methods.base import AliceMethod
from aliceio.types import UploadedImagesList


class GetImages(AliceMethod[UploadedImagesList]):
    __returning__ = UploadedImagesList
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer) -> str:
        if self.skill is None:
            raise MethodNotMountedToSkillError
        return api_server.get_all_files_url(
            skill_id=self.skill.id,
            file_type=FileType.IMAGES,
        )
