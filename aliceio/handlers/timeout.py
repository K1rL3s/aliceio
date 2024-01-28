from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import Session, TimeoutUpdate, User


class TimeoutHandler(BaseHandler[TimeoutUpdate], ABC):
    """Базовый класс для обработчиков таймаут-событий."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.session.user

    @property
    def session(self) -> Session:
        return self.event.session
