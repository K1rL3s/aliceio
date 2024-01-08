from typing import Optional

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
    user: Optional[User]  # None если пользователь неавторизован
    application: Application
    new: bool
