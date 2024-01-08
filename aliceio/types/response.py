from typing import List, Optional

from .base import AliceObject
from .card import Card
from .directives import Directives
from .show_item_meta import ShowItemMeta
from .text_button import TextButton


class Response(AliceObject):
    """
    Ответ для API Алисы с полезной для пользователя информацией.

    https://yandex.ru/dev/dialogs/alice/doc/response.html#response__response-desc
    """

    text: str
    tts: Optional[str] = None
    card: Optional[Card] = None
    buttons: Optional[List[TextButton]] = None
    directives: Optional[Directives] = None
    show_item_meta: Optional[ShowItemMeta] = None
    should_listen: Optional[bool] = None
    end_session: bool = False
