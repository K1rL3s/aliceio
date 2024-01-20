from typing import TYPE_CHECKING, Any, Optional

from .base import AliceObject


class URL(AliceObject):
    """
    Ссылка на аудио или изображение в директиве аудио-плеера.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-art-desc

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-background-image-desc
    """  # noqa: E501

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
