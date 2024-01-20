from typing import TYPE_CHECKING, Any, List, Optional

from .base import AliceObject


class UploadedSound(AliceObject):
    """
    Загруженное аудио, доступное навыку.

    https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__upload-file

    https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__list
    """  # noqa: E501

    id: str
    skillId: str
    size: Optional[int]
    originalName: str
    createdAt: str
    isProcessed: bool
    error: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            id: str,
            skillId: str,
            size: Optional[int],
            originalName: str,
            createdAt: str,
            isProcessed: bool,
            error: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                id=id,
                skillId=skillId,
                size=size,
                originalName=originalName,
                createdAt=createdAt,
                isProcessed=isProcessed,
                error=error,
                **__pydantic_kwargs,
            )

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


class PreUploadedSound(AliceObject):
    """Ключ к аудио."""

    sound: UploadedSound

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            sound: UploadedSound,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                sound=sound,
                **__pydantic_kwargs,
            )


class UploadedSoundsList(AliceObject):
    """Список аудио."""

    sounds: List[UploadedSound]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            sounds: List[UploadedSound],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                sounds=sounds,
                **__pydantic_kwargs,
            )
