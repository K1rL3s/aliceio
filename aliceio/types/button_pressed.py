from typing import TYPE_CHECKING, Any, Optional

from .alice_event import AliceEvent
from .markup import Markup
from .nlu import NLU
from .payload import Payload
from .session import Session


class ButtonPressed(AliceEvent):
    """
    Нажатие пользователя на кнопку с непустым Payload.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-card-bigimage)
    """

    type: str
    payload: Payload
    markup: Optional[Markup] = None
    nlu: Optional[NLU] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            session: Session,  # из AliceEvent
            type: str,
            payload: Payload,
            markup: Optional[Markup] = None,
            nlu: Optional[NLU] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                type=type,
                payload=payload,
                markup=markup,
                nlu=nlu,
                **__pydantic_kwargs,
            )
