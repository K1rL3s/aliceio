from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import Purchase, Session, User


class PurchaseHandler(BaseHandler[Purchase], ABC):
    """Базовый класс для обработчиков покупок xd."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user

    @property
    def session(self) -> Session:
        return self.event.session
