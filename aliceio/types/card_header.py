from typing import Optional

from aliceio.types.base import MutableAliceObject


class CardHeader(MutableAliceObject):
    """
    Заголовок :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__header-desc
    """  # noqa

    text: Optional[str] = None  # Optional XD
