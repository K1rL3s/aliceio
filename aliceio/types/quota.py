from typing import TYPE_CHECKING, Any

from pydantic import computed_field

from .base import AliceObject


class Quota(AliceObject):
    """
    Доступный и израсходованный объём картинок или аудиофайлов. Значения в байтах.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html
    """

    total: int
    used: int

    if TYPE_CHECKING:
        def __init__(
            __pydantic_self__,
            *,
            total: int,
            used: int,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                total=total,
                used=used,
                **__pydantic_kwargs,
            )

    @computed_field  # type: ignore[misc]
    @property
    def available(self) -> int:
        return self.total - self.used


class PreQuota(AliceObject):
    """Ключ к квоте."""

    quota: Quota
