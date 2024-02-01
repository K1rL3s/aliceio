from typing import TYPE_CHECKING, Any, Dict

from aliceio.types.base import AliceObject

StateDict = Dict[str, Any]
SessionState = StateDict
UserState = StateDict
ApplicationState = StateDict
# https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html


class ApiState(AliceObject):
    """
    Данные о сохранённом состоянии на стороне API Алисы.

    [Source](https://yandex.ru/dev/dialogs/alice/doc/request.html#request__state-desc)
    """

    user: UserState
    session: SessionState
    application: ApplicationState

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            user: UserState,
            session: SessionState,
            application: ApplicationState,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                session=session,
                user=user,
                application=application,
                **__pydantic_kwargs,
            )
