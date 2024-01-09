from typing import Any, Optional, cast

from .base import MutableAliceObject
from .markup import Markup
from .nlu import NLU
from .payload import Payload


class Button(MutableAliceObject):
    """
    Нажатие пользователя на кнопку с непустым Payload.

    https://yandex.ru/dev/dialogs/alice/doc/request-buttonpressed.html
    """

    type: str
    payload: Payload
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None
