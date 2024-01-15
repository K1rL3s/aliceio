from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import ShowPull, User


class ShowPullHandler(BaseHandler[ShowPull], ABC):
    """Базовый класс для обработчиков запуска шоу Алисы."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user
