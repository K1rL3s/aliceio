from typing import Optional, Union

from aiohttp.web import Request as WebRequest

from aliceio.types import (
    AliceObject,
    Meta,
    Session,
    Request,
    Response,
    AliceResponse,
)
from aliceio.types.state import ApplicationState, AuthorizedUserState, SessionState


class AliceRequest(AliceObject):
    """
    Полный запрос от API Алисы.

    https://yandex.ru/dev/dialogs/alice/doc/request.html
    """

    original_request: WebRequest
    meta: Meta
    request: Request
    session: Session
    version: str

    def _make_alice_response(
        self,
        response: Response,
        session_state: Optional[SessionState] = None,
        user_state_update: Optional[AuthorizedUserState] = None,
        application_state: Optional[ApplicationState] = None,
    ) -> AliceResponse:
        return AliceResponse(
            response=response,
            session_state=session_state or {},
            user_state_update=user_state_update or {},
            application_state=application_state or {},
            version=self.version,
        )

    def response(
        self,
        response: Union[Response, str],
        session_state: Optional[SessionState] = None,
        user_state_update: Optional[AuthorizedUserState] = None,
        application_state: Optional[ApplicationState] = None,
        **kwargs,
    ) -> AliceResponse:
        """
        Generate response

        :param response: Response or Response's text:
            if response is not an instance of Response,
            it is passed to the Response init as text with kwargs.
            Otherwise it is used as a Response

        :param kwargs: tts, card, buttons, end_session for Response
            NOTE: if you want to pass card, consider using one of
              these methods: response_big_image, response_items_list

        :param session_state: Session's state
        :param user_state_update: User's state
        :param application_state: Application's state
            Allows to store data on Yandex's side
            Read more: https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html

        :return: AliceResponse
        """
        if not isinstance(response, Response):
            response = Response(text=response, **kwargs)

        return self._make_alice_response(
            response,
            session_state,
            user_state_update,
            application_state,
        )
