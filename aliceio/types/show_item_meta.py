from typing import TYPE_CHECKING, Any, Optional

from .base import MutableAliceObject


class ShowItemMeta(MutableAliceObject):
    """
    В ответе навык передает свойство :code`show_item_meta`.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/response-show-item-meta)
    """

    content_id: str
    publication_date: str
    title: Optional[str] = None
    title_tts: Optional[str] = None
    expiration_date: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            content_id: str,
            publication_date: str,
            title: Optional[str] = None,
            title_tts: Optional[str] = None,
            expiration_date: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                content_id=content_id,
                publication_date=publication_date,
                title=title,
                title_tts=title_tts,
                expiration_date=expiration_date,
                **__pydantic_kwargs,
            )
