from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import Button, User


class ButtonPressedHandler(BaseHandler[Button], ABC):
    """Базовый класс для обработчиков нажатий на кнопки."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user
