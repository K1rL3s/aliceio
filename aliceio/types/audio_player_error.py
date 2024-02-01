from typing import TYPE_CHECKING, Any

from .base import AliceObject


class AudioPlayerError(AliceObject):
    """
    Ошибка аудиоплеера.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html#request-audioplayer__playback-failed)
    """  # noqa: E501

    message: str
    type: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            message: str,
            type: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message=message,
                type=type,
                **__pydantic_kwargs,
            )
