from aliceio.types import AliceObject


class TokensEntity(AliceObject):
    """
    start и end из request.nlu.entities.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__entities-desc
    """  # noqa

    start: int
    end: int
