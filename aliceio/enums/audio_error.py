from aliceio.enums.base import StrEnum, ValuesEnum


class AudioErrorType(StrEnum, ValuesEnum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"
