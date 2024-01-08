from typing import Dict, Optional

from .audio_player_directive import AudioPlayerDirective
from .base import MutableAliceObject

StartAccountLinking = Dict
# https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html
# https://yandex.ru/dev/dialogs/alice/doc/auth/how-it-works.html


class Directives(MutableAliceObject):
    """
    Директивы.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html
    https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html
    """

    audio_player: Optional[AudioPlayerDirective] = None
    start_account_linking: Optional[StartAccountLinking] = None
