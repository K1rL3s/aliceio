from typing import Optional

from .audio_player_error import AudioPlayerError
from .base import MutableAliceObject


class AudioPlayer(MutableAliceObject):
    """
    Навык получает запрос с типом AudioPlayer,
    если пользователь произносит команду управления аудиоплеером
    или нажимает соответствующую кнопку в интерфейсе.

    https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    """

    type: str
    error: Optional[AudioPlayerError] = None
