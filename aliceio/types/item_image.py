from typing import Optional

from aliceio.types import AliceObject, MediaButton


class ItemImage(AliceObject):
    """
    Изображение в :class:`ItemsList`

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__items-desc
    """  # noqa

    image_id: str
    title: str
    description: str
    button: Optional[MediaButton] = None
