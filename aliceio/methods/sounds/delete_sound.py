from typing import Any, Dict

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.methods.base import AliceMethod
from aliceio.types import Result


class DeleteSound(AliceMethod[Result]):
    __returning__ = Result
    __http_method__ = HttpMethod.DELETE

    file_id: str

    def api_url(self, api_server: AliceAPIServer, skill_id: str) -> str:
        return api_server.get_file_url(
            skill_id=skill_id,
            file_type=FileType.SOUNDS,
            file_id=self.file_id,
        )

    def model_validate(self, data: Dict[str, Any], **kwargs: Any) -> Result:
        return Result.model_validate(data, **kwargs)
