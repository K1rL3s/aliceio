from abc import ABC
from typing import Optional

from aliceio.handlers.base import BaseHandler
from aliceio.types import AudioPlayer, Session, User


class AudioPlayerHandler(BaseHandler[AudioPlayer], ABC):
    """Базовый класс для обработчиков аудиоплеера."""

    @property
    def from_user(self) -> Optional[User]:
        return self.event.user

    @property
    def session(self) -> Session:
        return self.event.session
