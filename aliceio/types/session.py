from typing import Optional

from aliceio.types import AliceObject
from aliceio.types.application import Application
from aliceio.types.user import User


class Session(AliceObject):
    """Base Session object"""

    message_id: int
    session_id: str
    skill_id: str
    # user_id: str  DEPRECATED. Use `Session.application.application_id`
    user: Optional[User]  # None если пользователь неавторизован
    application: Application
    new: bool
