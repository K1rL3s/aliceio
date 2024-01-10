from typing import Any, Dict, List

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import UploadedImage


class GetImages(AliceMethod[List[UploadedImage]]):
    __returning__ = List[UploadedImage]
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.get_file_url(
            skill_id=skill_id,
            file_type=FileType.IMAGES,
            file_id="",
        )

    def model_validate(
        self,
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> List[UploadedImage]:
        return [
            UploadedImage.model_validate(image, **kwargs)
            for image in data[FileType.IMAGES]
        ]
