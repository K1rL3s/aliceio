from .base import AliceObject
from .quota import Quota


class SpaceStatus(AliceObject):
    """
    Оставшееся место в байтах для изображений и звуков.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__quota
    """

    images: Quota
    sounds: Quota
