from typing import TYPE_CHECKING, Any, Literal, Optional

from .base import AliceObject
from .interfaces import Interfaces

# TODO: Возможно flags появляется при запуске со станций, надо уточнить
# https://github.com/mahenzon/aioalice/blob/e66615138bf6ae4883154de7fe19a9f8c8c065bc/tests/_dataset.py#L216
POSSIBLE_FLAGS = Literal["no_cards_support"]


class Meta(AliceObject):
    """
    Информация об устройстве, с которого пользователь разговаривает с Алисой.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request#meta-desc)
    """

    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces
    flags: Optional[list[POSSIBLE_FLAGS]] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            locale: str,
            timezone: str,
            client_id: str,
            interfaces: Interfaces,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                locale=locale,
                timezone=timezone,
                client_id=client_id,
                interfaces=interfaces,
                **__pydantic_kwargs,
            )
