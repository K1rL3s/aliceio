from typing import TYPE_CHECKING, Any, Dict, Optional

from .audio_player_directive import AudioPlayerDirective
from .base import MutableAliceObject

StartAccountLinking = Dict[str, Any]
# https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html
# https://yandex.ru/dev/dialogs/alice/doc/auth/how-it-works.html


class Directives(MutableAliceObject):
    """
    Директивы.

    [Source 1](https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html)
    [Source 2](https://yandex.ru/dev/dialogs/alice/doc/response-start-account-linking.html)
    """  # noqa: E501

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
