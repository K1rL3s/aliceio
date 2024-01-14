from typing import Optional

from .base import AliceObject


class UploadedSound(AliceObject):
    """
    Загруженное аудио, доступное навыку.

    https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__upload-file

    https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__list
    """  # noqa

    id: str
    skillId: str
    size: Optional[int]
    originalName: str
    createdAt: str
    isProcessed: bool
    error: Optional[str]

    @property
    def skill_id(self) -> str:
        return self.skillId

    @property
    def original_name(self) -> str:
        return self.originalName

    @property
    def created_at(self) -> str:
        return self.createdAt

    @property
    def is_processed(self) -> bool:
        return self.isProcessed
