from typing import TYPE_CHECKING, Any

from .base import AliceObject


class Quota(AliceObject):
    """
    Доступный и израсходованный объём картинок или аудиофайлов. Значения в байтах.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload)
    """

    total: int
    used: int

    if TYPE_CHECKING:
        available: int

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

    else:

        @property
        def available(self) -> int:
            return self.total - self.used


class PreQuota(AliceObject):
    """Ключ к квоте."""

    quota: Quota

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            quota: Quota,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                quota=quota,
                **__pydantic_kwargs,
            )
