from typing import TYPE_CHECKING, Any

from .base import AliceObject
from .quota import PreQuota


class SpaceStatus(AliceObject):
    """
    Оставшееся место в байтах для изображений и звуков.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload#quota)
    """

    images: PreQuota
    sounds: PreQuota

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            images: PreQuota,
            sounds: PreQuota,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                images=images,
                sounds=sounds,
                **__pydantic_kwargs,
            )
