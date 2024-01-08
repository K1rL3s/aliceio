from typing import List

from ..types import UploadedImage
from .base import AliceMethod


class Images(AliceMethod[List[UploadedImage]]):
    __returning__ = List[UploadedImage]
    __api_method__ = "skills/{{skill_id}}/images"
