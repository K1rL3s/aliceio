from aliceio.enums.base import StrEnum


class FileType(StrEnum):
    """
    Вспомогательный енум для типов данных.
    Используется в генерации urlов апишки и для извлечения данных с jsonов.
    """

    IMAGES = "images"
    SOUNDS = "sounds"
    IMAGE = "image"
    SOUND = "sound"
