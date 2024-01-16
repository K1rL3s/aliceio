from abc import ABC
from typing import TYPE_CHECKING, Any, Optional

from aliceio.types.base import MutableAliceObject
from aliceio.types.session import Session
from aliceio.types.user import User


class AliceEvent(MutableAliceObject, ABC):
    session: Session
    user: Optional[User]

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            session: Session,
            user: Optional[User] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                user=user,
                session=session,
                **__pydantic_kwargs,
            )

    @property
    def from_user(self) -> Optional[User]:
        return self.user
