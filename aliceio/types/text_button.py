from typing import Optional

from .base import MutableAliceObject
from .payload import Payload


class TextButton(MutableAliceObject):
    """
    Кнопка под сообщением навыка или над клавиатурой пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__buttons-desc
    """

    title: str
    url: Optional[str] = None
    payload: Optional[Payload] = None
    hide: bool = True
