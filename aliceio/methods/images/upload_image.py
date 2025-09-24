from typing import TYPE_CHECKING, Any, Optional

from aliceio.client.alice import AliceAPIServer
from aliceio.enums import FileType, HttpMethod
from aliceio.exceptions import AliceWrongFieldError, MethodNotMountedToSkillError
from aliceio.methods.base import AliceMethod
from aliceio.types import InputFile, PreUploadedImage


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

    def model_post_init(self, context: Any, /) -> None:
        super().model_post_init(context)
        if self.file is None and self.url is None:
            raise AliceWrongFieldError('At least "file" or "url" must be not None')
        if self.file and self.url:
            raise AliceWrongFieldError('"file" and "url" cannot be specified together')

    def api_url(self, api_server: AliceAPIServer) -> str:
        if self.skill is None:
            raise MethodNotMountedToSkillError
        return api_server.upload_file_url(
            skill_id=self.skill.id,
            file_type=FileType.IMAGES,
        )
