from typing import TYPE_CHECKING, Any

from .alice_event import AliceEvent
from .session import Session


class ShowPull(AliceEvent):
    """
    Навык получает запрос с типом Show.Pull,
    если пользователь произносит команду запуска утреннего шоу Алисы.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request-show-pull)
    """

    type: str
    show_type: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            session: Session,  # из AliceEvent
            type: str,
            show_type: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                type=type,
                show_type=show_type,
                **__pydantic_kwargs,
            )
