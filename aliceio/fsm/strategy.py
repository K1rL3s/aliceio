from typing import Optional, Tuple

from aliceio.enums.base import StrEnum


class FSMStrategy(StrEnum):
    USER = "user"
    SESSION = "session"
    APPLICATION = "application"


def apply_strategy(
    strategy: FSMStrategy,
    user_id: str,
    session_id: str,
    application_id: str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if strategy == FSMStrategy.USER:
        return user_id, None, None
    if strategy == FSMStrategy.SESSION:
        return None, session_id, None
    if strategy == FSMStrategy.APPLICATION:
        return None, None, application_id
    return None, session_id, None  # Пусть по сессии, если суета
