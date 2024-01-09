from typing import Any, Dict

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
