from typing import Any, Dict

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, UploadedImage


class UploadImage(AliceMethod[UploadedImage]):
    __returning__ = UploadedImage
    __http_method__ = HttpMethod.POST

    file: InputFile

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.upload_url(skill_id=skill_id, file_type=FileType.IMAGES)

    def response_validate(self, data: Dict[str, Any], **kwargs: Any) -> UploadedImage:
        return UploadedImage.model_validate(data[FileType.IMAGE], **kwargs)
