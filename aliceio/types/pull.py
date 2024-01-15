from typing import TYPE_CHECKING, Any

from .alice_event import AliceEvent


class Pull(AliceEvent):
    """
    Навык получает запрос с типом Show.Pull,
    если пользователь произносит команду запуска утреннего шоу Алисы.

    https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    """

    type: str
    show_type: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            show_type: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                show_type=show_type,
                **__pydantic_kwargs,
            )
