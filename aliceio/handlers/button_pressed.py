from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import ButtonPressed, Session, User


class ButtonPressedHandler(BaseHandler[ButtonPressed], ABC):
    """Базовый класс для обработчиков нажатий на кнопки."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user

    @property
    def session(self) -> Session:
        return self.event.session
