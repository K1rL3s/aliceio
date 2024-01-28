from typing import TYPE_CHECKING, Any, Optional

from aliceio.types.base import MutableAliceObject

from .analytics import Analytics
from .api_state import ApplicationState, SessionState, UserState
from .response import Response


class AliceResponse(MutableAliceObject):
    """
    Ответ на запрос API Алисы.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/response.html)
    """

    response: Response

    session_state: Optional[SessionState] = None
    user_state_update: Optional[UserState] = None
    application_state: Optional[ApplicationState] = None
    analytics: Optional[Analytics] = None

    version: str = "1.0"

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            response: Response,
            session_state: Optional[SessionState] = None,
            user_state_update: Optional[UserState] = None,
            application_state: Optional[ApplicationState] = None,
            analytics: Optional[Analytics] = None,
            version: str = "1.0",
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                response=response,
                session_state=session_state,
                user_state_update=user_state_update,
                application_state=application_state,
                analytics=analytics,
                version=version,
                **__pydantic_kwargs,
            )
