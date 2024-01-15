from abc import ABC
from typing import TYPE_CHECKING, Any

from aliceio.types.base import MutableAliceObject
from aliceio.types.session import Session
from aliceio.types.user import User


class AliceEvent(MutableAliceObject, ABC):
    user: User
    session: Session

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            user: User,
            session: Session,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                user=user,
                session=session,
                **__pydantic_kwargs,
            )

    @property
    def from_user(self) -> User:
        return self.user
