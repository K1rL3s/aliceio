from typing import Dict, Optional

from aliceio.types import AliceObject, AudioPlayer


StartAccountLinking = Dict
# https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html
# https://yandex.ru/dev/dialogs/alice/doc/auth/how-it-works.html


class Directives(AliceObject):
    """
    Директивы.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html
    https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html
    """

    audio_player: Optional[AudioPlayer] = None
    start_account_linking: Optional[StartAccountLinking] = None
