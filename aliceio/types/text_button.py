from typing import Optional

from aliceio.types import AliceObject
from aliceio.types.payload import Payload


class TextButton(AliceObject):
    """
    Кнопка под сообщением навыка или над клавиатурой пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__buttons-desc
    """

    title: str
    url: Optional[str] = None
    payload: Optional[Payload] = None
    hide: bool = True
