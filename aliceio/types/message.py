from typing import TYPE_CHECKING, Any, Optional

from .alice_event import AliceEvent
from .markup import Markup
from .nlu import NLU
from .payload import Payload
from .session import Session


class Message(AliceEvent):
    """
    :class:`AliceRequest` с типом :code:`SimpleUtterance`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request-simpleutterance)
    """

    type: str
    command: str
    original_utterance: str
    payload: Optional[Payload] = None
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None

    if TYPE_CHECKING:
        text: str
        original_text: str
        original_command: str

        def __init__(
            __pydantic_self__,
            *,
            session: Session,  # из AliceEvent
            type: str,
            command: str,
            original_utterance: str,
            payload: Optional[Payload] = None,
            markup: Optional[Markup] = None,
            nlu: Optional[NLU] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                type=type,
                command=command,
                original_utterance=original_utterance,
                payload=payload,
                markup=markup,
                nlu=nlu,
                **__pydantic_kwargs,
            )

    else:

        @property
        def text(self) -> str:
            return self.command

        @property
        def original_text(self) -> str:
            return self.original_utterance

        @property
        def original_command(self) -> str:
            return self.original_utterance
