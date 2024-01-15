from typing import Any, Dict, TYPE_CHECKING

from aliceio.types.base import AliceObject

AccountLinking = Dict[str, Any]
Payments = Dict[str, Any]
Screen = Dict[str, Any]


class Interfaces(AliceObject):
    """
    Интерфейсы, доступные на устройстве пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__interfaces-desc
    """

    account_linking: AccountLinking
    payments: Payments
    screen: Screen

    if TYPE_CHECKING:
        def __init__(
            __pydantic_self__,
            *,
            account_linking: AccountLinking,
            payments: Payments,
            screen: Screen,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                account_linking=account_linking,
                payments=payments,
                screen=screen,
                **__pydantic_kwargs,
            )
