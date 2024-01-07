from typing import TYPE_CHECKING

from aliceio.types.base import AliceObject

if TYPE_CHECKING:
    from .alice_request import Update


class ErrorEvent(AliceObject):
    """Внутренннее событие, используется для получения ошибок при обработке событий."""

    alice_request: Update
    exception: Exception
