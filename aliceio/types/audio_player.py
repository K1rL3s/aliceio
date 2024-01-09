from typing import Optional

from .alice_event import AliceEvent
from .audio_player_error import AudioPlayerError


class AudioPlayer(AliceEvent):
    """
    Навык получает запрос с типом AudioPlayer,
    если пользователь произносит команду управления аудиоплеером
    или нажимает соответствующую кнопку в интерфейсе.

    https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    """

    type: str
    error: Optional[AudioPlayerError] = None
