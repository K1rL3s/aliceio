from typing import Optional

from aliceio.types import AliceObject, MediaButton


class CardFooter(AliceObject):
    """
    Текст и кнопки под `ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__footer-desc
    """  # noqa

    text: str
    button: Optional[MediaButton] = None
