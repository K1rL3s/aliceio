from typing import Optional

from aliceio.types import AliceObject
from aliceio.types.payload import Payload


class MediaButton(AliceObject):
    """
    Кнопка на изображении из :class:`ImageGallery` и :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-imagegallery.html#response-card-imagegallery__items-button-desc

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-button-desc
    """  # noqa

    text: str
    url: str
    payload: Optional[Payload] = None
