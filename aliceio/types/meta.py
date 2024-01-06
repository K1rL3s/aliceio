from aliceio.types import AliceObject, Interfaces


class Meta(AliceObject):
    """
    Информация об устройстве, с которого пользователь разговаривает с Алисой.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__meta-desc
    """

    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces
