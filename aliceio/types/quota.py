from pydantic import computed_field

from aliceio.types import AliceObject


class Quota(AliceObject):
    """
    Доступный и израсходованный объём картинок или аудиофайлов. Значения в байтах.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html
    """

    total: int
    used: int

    @computed_field
    @property
    def available(self) -> int:
        return self.total - self.used
