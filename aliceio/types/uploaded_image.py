from typing import TYPE_CHECKING, Any, Optional

from .base import AliceObject


class UploadedImage(AliceObject):
    """
    Загруженное изображение, доступное навыку.

    [Source 1](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload#download-internet)

    [Source 2](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload#upload-file)

    [Source 3](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload#list)
    """

    id: str
    size: int
    origUrl: Optional[str] = None
    # origUrl будет None если изображение загружено через файл, то есть не через url.
    createdAt: str

    if TYPE_CHECKING:
        orig_url: Optional[str]
        created_at: str

        def __init__(
            __pydantic_self__,
            *,
            id: str,
            size: int,
            origUrl: Optional[str] = None,
            createdAt: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                id=id,
                size=size,
                origUrl=origUrl,
                createdAt=createdAt,
                **__pydantic_kwargs,
            )

    else:

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

    images: list[UploadedImage]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            images: list[UploadedImage],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                images=images,
                **__pydantic_kwargs,
            )
