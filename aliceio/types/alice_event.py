from abc import ABC
from typing import TYPE_CHECKING, Any, Optional

from aliceio.types.base import MutableAliceObject
from aliceio.types.session import Session
from aliceio.types.user import User


class AliceEvent(MutableAliceObject, ABC):
    session: Session

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            session: Session,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                **__pydantic_kwargs,
            )

    @property
    def from_user(self) -> Optional[User]:
        return self.session.user

    @property
    def user(self) -> Optional[User]:
        return self.session.user
