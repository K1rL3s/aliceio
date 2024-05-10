from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .url import URL


class Metadata(MutableAliceObject):
    """
    Метадата аудиоплеера.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-metadata-desc)
    """

    title: Optional[str] = None
    sub_title: Optional[str] = None
    art: Optional[URL] = None
    background_image: Optional[URL] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            title: Optional[str] = None,
            sub_title: Optional[str] = None,
            art: Optional[URL] = None,
            background_image: Optional[URL] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                title=title,
                sub_title=sub_title,
                art=art,
                background_image=background_image,
                **__pydantic_kwargs,
            )
