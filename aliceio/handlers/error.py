from abc import ABC

from aliceio.handlers.base import BaseHandler


class ErrorHandler(BaseHandler[Exception], ABC):
    """Базовый класс для обработчиков исключений."""

    @property
    def exception_name(self) -> str:
        return self.event.__class__.__name__

    @property
    def exception_message(self) -> str:
        return str(self.event)
