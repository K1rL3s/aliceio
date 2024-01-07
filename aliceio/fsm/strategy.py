from enum import Enum, auto
from typing import Optional, Tuple


class FSMStrategy(Enum):
    USER = auto()
    SESSION = auto()


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
