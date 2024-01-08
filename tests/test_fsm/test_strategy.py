from typing import Tuple

import pytest

from aliceio.fsm.strategy import FSMStrategy, apply_strategy

SESSION_ID = "42:SESSION_ID"
USER_ID = "42:USER_ID"


class TestStrategy:
    @pytest.mark.parametrize(
        "strategy,expected",
        [
            [FSMStrategy.USER, (USER_ID, USER_ID)],
            [FSMStrategy.SESSION, (USER_ID, SESSION_ID)],
            [None, (USER_ID, SESSION_ID)]
        ],
    )
    def test_strategy(
        self,
        strategy: FSMStrategy,
        expected: Tuple[str, str, str],
    ) -> None:
        assert (
            apply_strategy(
                strategy=strategy,
                user_id=USER_ID,
                session_id=SESSION_ID,
            )
            == expected
        )
