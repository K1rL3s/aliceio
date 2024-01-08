from aliceio.types import AliceObject


class CardHeader(AliceObject):
    """
    Заголовок :class:`ItemsList`.

    https://yandex.ru/dev/dialogs/alice/doc/response-card-itemslist.html#response-card-itemslist__header-desc
    """  # noqa

    text: str
