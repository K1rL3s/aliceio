from typing import Optional, TYPE_CHECKING, Any

from .nlu_entity import NLUEntity


class FIOEntity(NLUEntity):
    """
    NLU Entity Фамилии, имени и отчества.

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__fio
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
