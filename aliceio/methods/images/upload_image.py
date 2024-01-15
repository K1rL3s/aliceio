from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, PreUploadedImage


class UploadImage(AliceMethod[PreUploadedImage]):
    __returning__ = PreUploadedImage
    __http_method__ = HttpMethod.POST

    file: InputFile

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.upload_file_url(skill_id=skill_id, file_type=FileType.IMAGES)
