from typing import Any, Dict

from ..client.alice import AliceAPIServer
from ..enums import FileType, HttpMethod
from ..types import Quota, SpaceStatus
from .base import AliceMethod


class Status(AliceMethod[SpaceStatus]):
    __returning__ = SpaceStatus
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.api_url(method="status")

    def model_validate(self, data: Dict[str, Any], **kwargs) -> SpaceStatus:
        return SpaceStatus(
            images=Quota.model_validate(data[FileType.IMAGES]["quota"]),
            sounds=Quota.model_validate(data[FileType.SOUNDS]["quota"]),
            **kwargs,
        )
