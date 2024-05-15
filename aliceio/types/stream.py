from typing import TYPE_CHECKING, Any

from .base import MutableAliceObject


class Stream(MutableAliceObject):
    """
    Описание аудиопотока.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-stream-desc)
    """

    url: str
    offset_ms: int
    token: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            url: str,
            offset_ms: int,
            token: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                url=url,
                offset_ms=offset_ms,
                token=token,
                **__pydantic_kwargs,
            )
