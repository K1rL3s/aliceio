from aliceio.types.base import AliceObject


class Result(AliceObject):
    """
    Ответ на удаление файла.

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__delete

    https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__delete
    """  # noqa

    result: str
