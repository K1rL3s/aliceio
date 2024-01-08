from aliceio.enums.base import ValuesEnum

from .base import AliceObject


class AudioPlayerError(AliceObject):
    """Ошибка аудиоплеера.

    https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html#request-audioplayer__playback-failed
    """  # noqa

    message: str
    type: str


class ErrorType(str, ValuesEnum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"
