from typing import TYPE_CHECKING, Any, List, Optional

from .base import AliceObject


class UploadedImage(AliceObject):
    """
    Загруженное изображение, доступное навыку.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__download-internet

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__upload-file

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__list
    """  # noqa: E501

    id: str
    origUrl: Optional[str] = None
    # origUrl будет None если изображение загружено через файл, то есть не через url.
    size: int
    createdAt: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            id: str,
            origUrl: Optional[str] = None,
            size: int,
            createdAt: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                id=id,
                origUrl=origUrl,
                size=size,
                createdAt=createdAt,
                **__pydantic_kwargs,
            )

    @property
    def orig_url(self) -> Optional[str]:
        return self.origUrl

    @property
    def created_at(self) -> str:
        return self.createdAt


class PreUploadedImage(AliceObject):
    """Ключ к изображению."""

    image: UploadedImage

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            image: UploadedImage,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                image=image,
                **__pydantic_kwargs,
            )


class UploadedImagesList(AliceObject):
    """Список с изображениями."""

    images: List[UploadedImage]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            images: List[UploadedImage],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                images=images,
                **__pydantic_kwargs,
            )
