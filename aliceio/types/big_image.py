from typing import Optional

from aliceio.types import Card, CardType, MediaButton


class BigImage(Card):
    """
    :class:`Card` с типом :code:`BigImage`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-bigimage.html
    """

    type: str = CardType.BIG_IMAGE

    image_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[MediaButton] = None
