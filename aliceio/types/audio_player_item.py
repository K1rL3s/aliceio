from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject
from .metadata import Metadata
from .stream import Stream


class AudioPlayerItem(MutableAliceObject):
    """
    Данные директивы аудиоплеера.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-audio-player#audio-player-item-desc)
    """

    stream: Stream
    metadata: Optional[Metadata] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            stream: Stream,
            metadata: Optional[Metadata] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                stream=stream,
                metadata=metadata,
                **__pydantic_kwargs,
            )
