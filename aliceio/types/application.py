from aliceio.types import AliceObject


class Application(AliceObject):
    """
    Приложение из Session.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__application-desc
    """

    application_id: str
