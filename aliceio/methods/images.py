from typing import List

from .base import AliceMethod
from ..types import UploadedImage


class Images(AliceMethod[List[UploadedImage]]):
    __returning__ = List[UploadedImage]
    __api_method__ = "skills/{{skill_id}}/images"
