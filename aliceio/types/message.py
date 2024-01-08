from typing import Optional, cast

from .base import MutableAliceObject
from .markup import Markup
from .nlu import NLU
from .payload import Payload


class Message(MutableAliceObject):
    """
    :class:`AliceRequest` с типом :code:`SimpleUtterance`.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html
    """

    type: str
    payload: Payload
    command: Optional[str] = None
    original_utterance: Optional[str] = None
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None

    def __post_init__(self):
        if self.markup is not None:
            self.markup = Markup(**cast(dict, self.markup))
