from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import Result


class DeleteImage(AliceMethod[Result]):
    __returning__ = Result
    __http_method__ = HttpMethod.DELETE

    file_id: str

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.delete_file_url(
            skill_id=skill_id,
            file_type=FileType.IMAGES,
            file_id=self.file_id,
        )
