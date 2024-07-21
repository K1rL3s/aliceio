from typing import TYPE_CHECKING, Any

from .base import AliceObject
from .interfaces import Interfaces


class Meta(AliceObject):
    """
    Информация об устройстве, с которого пользователь разговаривает с Алисой.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request#meta-desc)
    """

    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces

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
