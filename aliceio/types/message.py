from typing import TYPE_CHECKING, Any, ClassVar, Optional

from .alice_event import AliceEvent
from .markup import Markup
from .nlu import NLU
from .payload import Payload
from .session import Session


class Message(AliceEvent):
    """
    :class:`AliceRequest` с типом :code:`SimpleUtterance`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html)
    """

    type: str
    command: str
    original_utterance: str
    payload: Optional[Payload] = None
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None

    if TYPE_CHECKING:
        text: ClassVar[str]
        original_text: ClassVar[str]
        original_command: ClassVar[str]

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            command: str,
            original_utterance: str,
            session: Session,  # из AliceEvent
            payload: Optional[Payload] = None,
            markup: Optional[Markup] = None,
            nlu: Optional[NLU] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                command=command,
                original_utterance=original_utterance,
                session=session,
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
