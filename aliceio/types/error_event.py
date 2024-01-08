from .base import AliceObject
from .update import Update


class ErrorEvent(AliceObject):
    """Внутренннее событие, используется для получения ошибок при обработке событий."""

    update: Update
    exception: Exception
