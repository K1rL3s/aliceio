from aliceio.enums.base import ValuesEnum


class AudioErrorType(str, ValuesEnum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"
