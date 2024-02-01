from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from aliceio.types.base import MutableAliceObject
from aliceio.types.session import Session
from aliceio.types.user import User


class AliceEvent(MutableAliceObject, ABC):
    """
    Родительский класс для событий от Алисы.
    """

    session: Session

    if TYPE_CHECKING:
        from_user: ClassVar[Optional[User]]
        user: ClassVar[Optional[User]]

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

    else:

        @property
        def from_user(self) -> Optional[User]:
            return self.session.user

        @property
        def user(self) -> Optional[User]:
            return self.session.user
