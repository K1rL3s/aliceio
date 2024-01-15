from typing import TYPE_CHECKING, Any, Optional

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

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            command: str,
            original_utterance: str,
            payload: Optional[Payload] = None,
            markup: Optional[Markup] = None,
            nlu: Optional[NLU] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                command=command,
                original_utterance=original_utterance,
                payload=payload,
                markup=markup,
                nlu=nlu,
                **__pydantic_kwargs,
            )
