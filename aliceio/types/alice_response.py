from typing import Optional

from aliceio.types import AliceObject, Response
from aliceio.types.analytics import Analytics
from aliceio.types.state import ApplicationState, AuthorizedUserState, SessionState


class AliceResponse(AliceObject):
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
