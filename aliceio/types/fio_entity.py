from typing import TYPE_CHECKING, Any, Optional

from .nlu_entity import NLUEntity


class FIOEntity(NLUEntity):
    """
    NLU Entity Фамилии, имени и отчества.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/naming-entities#fio)
    """

    first_name: Optional[str] = None
    patronymic_name: Optional[str] = None
    last_name: Optional[str] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            first_name: Optional[str] = None,
            patronymic_name: Optional[str] = None,
            last_name: Optional[str] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                first_name=first_name,
                patronymic_name=patronymic_name,
                last_name=last_name,
                **__pydantic_kwargs,
            )
