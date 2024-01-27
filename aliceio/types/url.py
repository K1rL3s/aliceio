from typing import TYPE_CHECKING, Any, Optional

from .base import AliceObject


class URL(AliceObject):
    """
    Ссылка на [аудио](https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-art-desc) или [изображение](https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-background-image-desc) в директиве аудио-плеера.
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
