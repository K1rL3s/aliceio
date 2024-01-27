from typing import TYPE_CHECKING, Any

from aliceio.types.base import MutableAliceObject


class Application(MutableAliceObject):
    """
    [Приложение](https://yandex.ru/dev/dialogs/alice/doc/request.html#request__application-desc) из :class:`Session`.
    """

    application_id: str

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            application_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                application_id=application_id,
                **__pydantic_kwargs,
            )
