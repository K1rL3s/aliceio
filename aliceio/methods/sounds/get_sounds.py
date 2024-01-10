from typing import Any, Dict, List

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import UploadedSound


class GetSounds(AliceMethod[List[UploadedSound]]):
    __returning__ = List[UploadedSound]
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.get_file_url(
            skill_id=skill_id,
            file_type=FileType.SOUNDS,
            file_id="",
        )

    def model_validate(
        self,
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> List[UploadedSound]:
        return [
            UploadedSound.model_validate(sound, **kwargs)
            for sound in data[FileType.SOUNDS]
        ]
