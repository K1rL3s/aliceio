from typing import Optional

from aliceio.enums.base import StrEnum


class FSMStrategy(StrEnum):
    """
    API Яндекс Диалогов позволяет сохранять данные внутри сессии навыка, а если
    пользователь авторизован на поверхности, где работает навык, — то и между сессиями.

    Примечание:
    Если навыком пользуется неавторизованный пользователь, то FSMStrategy.USER будет как
     FSMStrategy.APPLICATION:
    - для локальных хранилищ user_id будет равен application_id
    - в хранилище на стороне Алисы состояние будет храниться по устройству
    """

    USER = "user"
    """Хранение состояния по юзеру"""
    SESSION = "session"
    """Хранение состояния по сессии"""
    APPLICATION = "application"
    """Хранение состояния по устройству"""


def apply_strategy(
    strategy: FSMStrategy,
    user_id: str,
    session_id: str,
    application_id: str,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    if strategy == FSMStrategy.USER:
        return user_id, None, None
    if strategy == FSMStrategy.SESSION:
        return None, session_id, None
    if strategy == FSMStrategy.APPLICATION:
        return None, None, application_id
    return None, session_id, None  # Пусть по сессии, если суета
