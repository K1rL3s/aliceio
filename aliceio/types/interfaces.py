from typing import Any, Dict, Optional

from aliceio.types.base import AliceObject

AccountLinking = Dict[str, Any]
Screen = Dict[str, Any]
AudioPlayer = Dict[str, Any]


class Interfaces(AliceObject):
    """
    Интерфейсы, доступные на устройстве пользователя.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__interfaces-desc
    """

    account_linking: Optional[AccountLinking] = None
    screen: Optional[Screen] = None
    audio_player: Optional[AudioPlayer] = None
