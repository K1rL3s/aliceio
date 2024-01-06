from aliceio.types import AliceObject


class User(AliceObject):
    """Пользователь из Session"""

    user_id: str
    acess_token: str
