from typing import Any, Dict

from ..client.alice import AliceAPIServer
from ..enums import HttpMethod
from ..types import SpaceStatus
from .base import AliceMethod


class Status(AliceMethod[SpaceStatus]):
    __returning__ = SpaceStatus
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.api_url(method="status")

    def response_validate(self, data: Dict[str, Any], **kwargs: Any) -> SpaceStatus:
        return SpaceStatus.model_validate(data, **kwargs)
