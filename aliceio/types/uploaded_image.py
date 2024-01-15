from typing import List, Optional

from .base import AliceObject


class UploadedImage(AliceObject):
    """
    Загруженное изображение, доступное навыку.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__download-internet

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__upload-file

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__list
    """  # noqa

    id: str
    origUrl: Optional[str] = None
    # origUrl будет None если изображение загружено через файл, то есть не через url.
    size: int
    createdAt: str

    @property
    def orig_url(self) -> Optional[str]:
        return self.origUrl

    @property
    def created_at(self) -> str:
        return self.createdAt


class PreUploadedImage(AliceObject):
    """Ключ к изображению."""

    image: UploadedImage


class UploadedImagesList(AliceObject):
    """Список с изображениями."""

    images: List[UploadedImage]
