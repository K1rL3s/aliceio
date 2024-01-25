from typing import TYPE_CHECKING, Any, Optional

from .application import Application
from .base import AliceObject
from .user import User


class Session(AliceObject):
    """
    Информация о сессии в навыке.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__session-desc
    """

    message_id: int
    session_id: str
    skill_id: str
    # user_id: str  DEPRECATED. Use `Session.application.application_id`
    application: Application
    new: bool
    user: Optional[User] = None  # None если пользователь неавторизован

    if TYPE_CHECKING:

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
