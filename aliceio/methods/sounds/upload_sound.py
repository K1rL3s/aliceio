from typing import Any, Dict

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, UploadedSound


class UploadSound(AliceMethod[UploadedSound]):
    __returning__ = UploadedSound
    __http_method__ = HttpMethod.POST

    file: InputFile

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.upload_url(skill_id=skill_id, file_type=FileType.SOUNDS)

    def response_validate(self, data: Dict[str, Any], **kwargs: Any) -> UploadedSound:
        return UploadedSound.model_validate(data[FileType.SOUND], **kwargs)
