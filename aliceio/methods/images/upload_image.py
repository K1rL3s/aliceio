from typing import TYPE_CHECKING, Any, Optional, cast

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.exceptions import AliceWrongFieldError
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, PreUploadedImage

if TYPE_CHECKING:
    from aliceio.client.skill import Skill


class UploadImage(AliceMethod[PreUploadedImage]):
    __returning__ = PreUploadedImage
    __http_method__ = HttpMethod.POST

    # Только одно из полей должно быть
    file: Optional[InputFile] = None
    url: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            file: Optional[InputFile] = None,
            url: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                file=file,
                url=url,
                **__pydantic_kwargs,
            )

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if self.file is None and self.url is None:
            raise AliceWrongFieldError('At least "file" or "url" must be not None')
        if self.file and self.url:
            raise AliceWrongFieldError('"file" and "url" cannot be specified together')

    def api_url(self, api_server: AliceAPIServer) -> str:
        skill: Skill = cast("Skill", self.skill)
        return api_server.upload_file_url(
            skill_id=skill.id,
            file_type=FileType.IMAGES,
        )
