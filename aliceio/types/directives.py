from typing import Any, Dict, Optional, TYPE_CHECKING

from .audio_player_directive import AudioPlayerDirective
from .base import MutableAliceObject

StartAccountLinking = Dict[str, Any]
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

    if TYPE_CHECKING:
        def __init__(
            __pydantic_self__,
            *,
            audio_player: Optional[AudioPlayerDirective] = None,
            start_account_linking: Optional[StartAccountLinking] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                audio_player=audio_player,
                start_account_linking=start_account_linking,
                **__pydantic_kwargs,
            )
