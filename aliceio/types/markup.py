from typing import TYPE_CHECKING, Any

from aliceio.types.base import AliceObject


class Markup(AliceObject):
    """
    Формальные характеристики реплики, которые удалось выделить Яндекс Диалогам.
    Объект отсутствует, если ни одно из вложенных свойств не применимо.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__markup-desc)
    """

    dangerous_context: bool

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            dangerous_context: bool,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                dangerous_context=dangerous_context,
                **__pydantic_kwargs,
            )
