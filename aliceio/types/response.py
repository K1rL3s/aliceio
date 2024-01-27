from typing import TYPE_CHECKING, Any, List, Optional

from .base import AliceObject
from .card import Card
from .directives import Directives
from .show_item_meta import ShowItemMeta
from .text_button import TextButton


class Response(AliceObject):
    """
    [Ответ](https://yandex.ru/dev/dialogs/alice/doc/response.html#response__response-desc) для API Алисы с полезной для пользователя информацией.
    """

    text: str
    tts: Optional[str] = None
    card: Optional[Card] = None
    buttons: Optional[List[TextButton]] = None
    directives: Optional[Directives] = None
    show_item_meta: Optional[ShowItemMeta] = None
    should_listen: Optional[bool] = None
    end_session: bool = False

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            text: str,
            tts: Optional[str] = None,
            card: Optional[Card] = None,
            buttons: Optional[List[TextButton]] = None,
            directives: Optional[Directives] = None,
            show_item_meta: Optional[ShowItemMeta] = None,
            should_listen: Optional[bool] = None,
            end_session: bool = False,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                text=text,
                tts=tts,
                card=card,
                buttons=buttons,
                directives=directives,
                show_item_meta=show_item_meta,
                should_listen=should_listen,
                end_session=end_session,
                **__pydantic_kwargs,
            )
