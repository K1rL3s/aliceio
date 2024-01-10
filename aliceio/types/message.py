from typing import Optional

from .alice_event import AliceEvent
from .markup import Markup
from .nlu import NLU
from .payload import Payload


class Message(AliceEvent):
    """
    :class:`AliceRequest` с типом :code:`SimpleUtterance`.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html
    """

    type: str
    command: str
    original_utterance: str
    payload: Optional[Payload] = None
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None
