from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import Message, Session, User


class MessageHandler(BaseHandler[Message], ABC):
    """Базовый класс для обработчиков сообщений."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user

    @property
    def session(self) -> Session:
        return self.event.session
