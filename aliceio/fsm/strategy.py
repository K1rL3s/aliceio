from typing import Optional, Tuple

from aliceio.enums.base import StrEnum


class FSMStrategy(StrEnum):
    USER = "user"
    SESSION = "session"


def apply_strategy(
    strategy: FSMStrategy,
    user_id: str,
    session_id: str,
) -> Tuple[str, Optional[str]]:
    if strategy == FSMStrategy.USER:
        return user_id, user_id
    if strategy == FSMStrategy.SESSION:
        return user_id, session_id
    return user_id, session_id
