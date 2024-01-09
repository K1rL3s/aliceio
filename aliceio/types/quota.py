from pydantic import computed_field

from .base import AliceObject


class Quota(AliceObject):
    """
    Доступный и израсходованный объём картинок или аудиофайлов. Значения в байтах.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html
    """

    total: int
    used: int

    @computed_field  # type: ignore[misc]
    @property
    def available(self) -> int:
        return self.total - self.used
