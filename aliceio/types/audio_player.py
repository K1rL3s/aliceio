from typing import TYPE_CHECKING, Any, Optional

from .alice_event import AliceEvent
from .audio_player_error import AudioPlayerError
from .session import Session


class AudioPlayer(AliceEvent):
    """
    Навык получает запрос с типом AudioPlayer,
    если пользователь произносит команду управления аудиоплеером
    или нажимает соответствующую кнопку в интерфейсе.

    https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    """

    type: str
    error: Optional[AudioPlayerError] = None

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            type: str,
            session: Session,  # из AliceEvent
            error: Optional[AudioPlayerError] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                session=session,
                error=error,
                **__pydantic_kwargs,
            )
