from ..client.alice import AliceAPIServer
from ..enums import HttpMethod
from ..types import SpaceStatus
from .base import AliceMethod


class Status(AliceMethod[SpaceStatus]):
    __returning__ = SpaceStatus
    __http_method__ = HttpMethod.GET

    def api_url(self, api_server: AliceAPIServer) -> str:
        return api_server.api_url(method="status")
