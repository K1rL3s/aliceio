from typing import Optional

from .base import MutableAliceObject
from .media_button import MediaButton


class CardFooter(MutableAliceObject):
    """
    Текст и кнопки под :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__footer-desc
    """  # noqa

    text: Optional[str] = None  # Optional XD
    button: Optional[MediaButton] = None
