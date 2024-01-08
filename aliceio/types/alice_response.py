from typing import Optional

from aliceio.types.base import MutableAliceObject

from .analytics import Analytics
from .response import Response
from .state import ApplicationState, AuthorizedUserState, SessionState


class AliceResponse(MutableAliceObject):
    """
    Ответ на запрос API Алисы.

    https://yandex.ru/dev/dialogs/alice/doc/response.html
    """

    response: Response
    session_state: Optional[SessionState]
    user_state_update: Optional[AuthorizedUserState]
    application_state: Optional[ApplicationState]
    analytics: Optional[Analytics]
    version: str = "1.0"
