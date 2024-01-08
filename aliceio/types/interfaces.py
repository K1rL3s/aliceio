from typing import Dict

from aliceio.types.base import AliceObject

AccountLinking = Dict
Payments = Dict
Screen = Dict


class Interfaces(AliceObject):
    """
    Интерфейсы, доступные на устройстве пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__interfaces-desc
    """

    account_linking: AccountLinking
    payments: Payments
    screen: Screen
