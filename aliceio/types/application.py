from aliceio.types.base import MutableAliceObject


class Application(MutableAliceObject):
    """
    Приложение из :class:`Session`.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__application-desc
    """

    application_id: str
