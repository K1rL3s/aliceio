from abc import ABC

from aliceio.types.base import MutableAliceObject
from aliceio.types.session import Session
from aliceio.types.user import User


class AliceEvent(MutableAliceObject, ABC):
    user: User
    session: Session

    @property
    def from_user(self) -> User:
        return self.user
