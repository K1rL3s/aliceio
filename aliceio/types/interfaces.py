from typing import TYPE_CHECKING, Any, Dict, Optional

from aliceio.types.base import AliceObject

AccountLinking = Dict[str, Any]
Screen = Dict[str, Any]
AudioPlayer = Dict[str, Any]


class Interfaces(AliceObject):
    """
    Интерфейсы, доступные на устройстве (поверхности) пользователя.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request#interfaces-desc)
    """

    account_linking: Optional[AccountLinking] = None
    screen: Optional[Screen] = None
    audio_player: Optional[AudioPlayer] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            account_linking: Optional[AccountLinking] = None,
            screen: Optional[Screen] = None,
            audio_player: Optional[AudioPlayer] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                account_linking=account_linking,
                screen=screen,
                audio_player=audio_player,
                **__pydantic_kwargs,
            )
