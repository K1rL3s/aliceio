from typing import TYPE_CHECKING, Any, Optional

from .base import AliceObject


class URL(AliceObject):
    """
    Ссылка на аудио или изображение в директиве аудио-плеера.

    [Source 1](https://yandex.ru/dev/dialogs/alice/doc/ru/response-audio-player#audio-player-item-metadata-art-desc)

    [Source 2](https://yandex.ru/dev/dialogs/alice/doc/ru/response-audio-player#audio-player-item-metadata-background-image-desc)
    """

    url: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            url: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                url=url,
                **__pydantic_kwargs,
            )
