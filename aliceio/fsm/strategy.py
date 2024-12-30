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
    """По этому ключу можно получить user_id"""
    SESSION = "session"
    """
    Хранение состояния сессии
    Чтобы сохранить данные внутри сессии, навык должен отправить свойство session_state
    в ответе. Записанное значение придет в следующем запросе в навык.
    Данные хранятся до конца сессии.
    """
    APPLICATION = "application"
    """
    Экземпляр приложения — это конкретное приложение (например, Браузер,
    приложение Яндекс, Навигатор) или устройство. Разрез хранения равносилен
    session.application.application_id для навыка.
    """


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
