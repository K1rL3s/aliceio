from typing import TYPE_CHECKING, Any, Optional

from aliceio.types.base import MutableAliceObject


class CardHeader(MutableAliceObject):
    """
    Заголовок :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__header-desc
    """  # noqa

    text: Optional[str] = None  # Optional XD

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            text: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                text=text,
                **__pydantic_kwargs,
            )
