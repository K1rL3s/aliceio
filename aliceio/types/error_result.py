from aliceio.types.base import AliceObject


class ErrorResult(AliceObject):
    """
    Сообщение об ошибке при запросах к API Алисы.

    Важно заметить, что если навык вернёт ответ пользователю в некорректном формате, то
    Алиса никак не оповестит об ошибке.
    """

    message: str
