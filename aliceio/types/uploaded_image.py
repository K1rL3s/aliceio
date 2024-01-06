from typing import Optional

from aliceio.types import AliceObject


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
    def orig_url(self) -> str:
        return self.origUrl

    @property
    def created_at(self) -> str:
        return self.createdAt
