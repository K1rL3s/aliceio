from .base import AliceMethod
from ..types import SpaceStatus


class Status(AliceMethod[SpaceStatus]):
    __returning__ = SpaceStatus
    __api_method__ = "status"
