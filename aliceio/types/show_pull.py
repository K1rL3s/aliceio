from .alice_event import AliceEvent


class ShowPull(AliceEvent):
    """
    Навык получает запрос с типом Show.Pull,
    если пользователь произносит команду запуска утреннего шоу Алисы.

    https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    """

    type: str
    show_type: str
