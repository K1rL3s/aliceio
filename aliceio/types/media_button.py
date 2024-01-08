from typing import Optional

from .base import MutableAliceObject
from .payload import Payload


class MediaButton(MutableAliceObject):
    """
    Кнопка на изображении из :class:`ImageGallery` и :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-button-desc

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-button-desc
    """  # noqa

    text: str
    url: str
    payload: Optional[Payload] = None
