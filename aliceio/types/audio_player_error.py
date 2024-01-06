from enum import Enum

from aliceio.types import AliceObject


class AudioPlayerError(AliceObject):
    """Ошибка аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html#request-audioplayer__playback-failed
    """  # noqa

    message: str
    type: str


class ErrorType(str, Enum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"
