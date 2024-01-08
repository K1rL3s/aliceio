from typing import Optional

from .nlu_entity import NLUEntity


class DateTimeEntity(NLUEntity):
    """
    NLU Entity Даты и времени.

    https://yandex.ru/dev/dialogs/alice/doc/naming-entities.html#naming-entities__datetime
    """  # noqa

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
