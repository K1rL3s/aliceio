from functools import cached_property
from typing import TYPE_CHECKING, Any, Optional

from typing_extensions import TypeAlias, TypedDict

from aliceio.types.base import AliceObject


class _EmptyDict(TypedDict):
    pass


AccountLinking: TypeAlias = _EmptyDict
Screen: TypeAlias = _EmptyDict
AudioPlayer: TypeAlias = _EmptyDict
Payments: TypeAlias = _EmptyDict


class Interfaces(AliceObject):
    """
    Интерфейсы, доступные на устройстве (поверхности) пользователя.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request#interfaces-desc)
    """

    account_linking: Optional[AccountLinking] = None
    screen: Optional[Screen] = None
    audio_player: Optional[AudioPlayer] = None
    payments: Optional[Payments] = None

    if TYPE_CHECKING:
        available_interfaces: set[str]
        available: set[str]

        def __init__(
            __pydantic_self__,
            *,
            account_linking: Optional[AccountLinking] = None,
            screen: Optional[Screen] = None,
            audio_player: Optional[AudioPlayer] = None,
            payments: Optional[Payments] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                account_linking=account_linking,
                screen=screen,
                audio_player=audio_player,
                payments=payments,
                **__pydantic_kwargs,
            )

    else:

        @cached_property
        def available_interfaces(self) -> set[str]:
            return {
                interface
                for interface in self.__annotations__
                if isinstance(getattr(self, interface, None), dict)
            }

        @property
        def available(self) -> set[str]:
            return self.available_interfaces

    def is_interface_available(self, interface: str) -> bool:
        return interface in self.available_interfaces

    def has(self, interface: str) -> bool:
        return self.is_interface_available(interface)
