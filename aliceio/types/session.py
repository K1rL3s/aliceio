from typing import TYPE_CHECKING, Any, ClassVar, Optional

from .application import Application
from .base import AliceObject
from .user import User


class Session(AliceObject):
    """
    Информация о сессии пользователя в навыке.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/ru/request#session-desc)
    """

    message_id: int
    session_id: str
    skill_id: str
    # user_id: str  DEPRECATED. Use `Session.application.application_id`
    application: Application
    new: bool
    user: Optional[User] = None  # None если пользователь неавторизован

    if TYPE_CHECKING:
        is_anonymous: ClassVar[bool]

        def __init__(
            __pydantic_self__,
            *,
            message_id: int,
            session_id: str,
            skill_id: str,
            # user_id: str,
            application: Application,
            new: bool,
            user: Optional[User] = None,  # None если пользователь неавторизован
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message_id=message_id,
                session_id=session_id,
                skill_id=skill_id,
                # user_id=user_id,
                user=user,
                application=application,
                new=new,
                **__pydantic_kwargs,
            )

    else:

        @property
        def is_anonymous(self) -> bool:
            return self.user is None
