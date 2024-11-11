from typing import TYPE_CHECKING, Any, Optional

from .audio_player_directive import AudioPlayerDirective
from .base import MutableAliceObject

StartAccountLinking = dict[str, Any]
# https://yandex.ru/dev/dialogs/alice/doc/ru/response-start-account-linking
# https://yandex.ru/dev/dialogs/alice/doc/ru/auth/how-it-works


class Directives(MutableAliceObject):
    """
    Директивы.

    [Source 1](https://yandex.ru/dev/dialogs/alice/doc/ru/response-audio-player)

    [Source 2](https://yandex.ru/dev/dialogs/alice/doc/ru/response-start-account-linking)
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
