from .base import AliceObject


class User(AliceObject):
    """
    Пользователь из :class:`Session`.

    https://yandex.ru/dev/dialogs/alice/doc/request.html#request__user-desc
    """

    user_id: str
    access_token: str
