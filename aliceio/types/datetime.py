from typing import TYPE_CHECKING, Any, Optional

from .nlu_entity import NLUEntity


class DateTimeEntity(NLUEntity):
    """
    NLU Entity Даты и времени.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__datetime)
    """

    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None

    year_is_relative: Optional[bool] = False
    month_is_relative: Optional[bool] = False
    day_is_relative: Optional[bool] = False
    hour_is_relative: Optional[bool] = False
    minute_is_relative: Optional[bool] = False

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            year: Optional[int] = None,
            month: Optional[int] = None,
            day: Optional[int] = None,
            hour: Optional[int] = None,
            minute: Optional[int] = None,
            year_is_relative: Optional[bool] = False,
            month_is_relative: Optional[bool] = False,
            day_is_relative: Optional[bool] = False,
            hour_is_relative: Optional[bool] = False,
            minute_is_relative: Optional[bool] = False,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                year_is_relative=year_is_relative,
                month_is_relative=month_is_relative,
                day_is_relative=day_is_relative,
                hour_is_relative=hour_is_relative,
                minute_is_relative=minute_is_relative,
                **__pydantic_kwargs,
            )
