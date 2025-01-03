from typing import Optional

from aliceio.enums.base import StrEnum


class FSMStrategy(StrEnum):
    """
    Возможность работает в тестовом режиме и активно развивается, поэтому протокол ее
    использования может меняться.
    API Яндекс Диалогов позволяет сохранять данные внутри сессии навыка, а если
    пользователь авторизован на поверхности, где работает навык, — то и между сессиями.
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
