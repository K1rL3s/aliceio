from ..types import SpaceStatus
from .base import AliceMethod


class Status(AliceMethod[SpaceStatus]):
    __returning__ = SpaceStatus
    __api_method__ = "status"
