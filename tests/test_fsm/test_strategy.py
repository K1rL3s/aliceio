from typing import Optional

import pytest

from aliceio.fsm.strategy import FSMStrategy, apply_strategy

SESSION_ID = "42:SESSION_ID"
USER_ID = "42:USER_ID"
APPLICATION_ID = "42:APP_ID"


class TestStrategy:
    @pytest.mark.parametrize(
        "strategy,expected",
        [
            [FSMStrategy.USER, (USER_ID, None, None)],
            [FSMStrategy.SESSION, (None, SESSION_ID, None)],
            [FSMStrategy.APPLICATION, (None, None, APPLICATION_ID)],
            [None, (None, SESSION_ID, None)],
        ],
    )
    def test_strategy(
        self,
        strategy: FSMStrategy,
        expected: tuple[Optional[str], Optional[str], Optional[str]],
    ) -> None:
        assert (
            apply_strategy(
                strategy=strategy,
                user_id=USER_ID,
                session_id=SESSION_ID,
                application_id=APPLICATION_ID,
            )
            == expected
        )
