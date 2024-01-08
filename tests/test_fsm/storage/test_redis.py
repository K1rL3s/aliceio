from typing import Final, Literal

import pytest

from aliceio.fsm.storage.base import DEFAULT_DESTINY, StorageKey
from aliceio.fsm.storage.redis import DefaultKeyBuilder

PREFIX = "test"
SKILL_ID = "42:SKILL_ID"
USER_ID = "42:USER_ID"
SESSION_ID = "42:SESSION_ID"
FIELD: Final[Literal["data"]] = "data"


class TestRedisDefaultKeyBuilder:
    @pytest.mark.parametrize(
        "with_session_id,with_destiny,result",
        [
            [False, False, f"{PREFIX}:{SKILL_ID}:{USER_ID}:{FIELD}"],
            [False, True, f"{PREFIX}:{SKILL_ID}:{USER_ID}:{DEFAULT_DESTINY}:{FIELD}"],
            [True, False, f"{PREFIX}:{SKILL_ID}:{USER_ID}:{SESSION_ID}:{FIELD}"],
            [
                True,
                True,
                f"{PREFIX}:{SKILL_ID}:{USER_ID}:{SESSION_ID}:{DEFAULT_DESTINY}:{FIELD}",
            ],
        ],
    )
    async def test_generate_key(
        self,
        with_session_id: bool,
        with_destiny: bool,
        result: str,
    ) -> None:
        key_builder = DefaultKeyBuilder(
            prefix=PREFIX,
            with_session_id=with_session_id,
            with_destiny=with_destiny,
        )
        key = StorageKey(
            skill_id=SKILL_ID,
            user_id=USER_ID,
            session_id=SESSION_ID,
            destiny=DEFAULT_DESTINY,
        )
        assert key_builder.build(key, FIELD) == result

    async def test_destiny_check(self) -> None:
        key_builder = DefaultKeyBuilder(
            with_destiny=False,
        )
        key = StorageKey(skill_id=SKILL_ID, user_id=USER_ID, session_id=SESSION_ID)
        assert key_builder.build(key, FIELD)

        key = StorageKey(
            skill_id=SKILL_ID,
            user_id=USER_ID,
            session_id=SESSION_ID,
            destiny="CUSTOM_TEST_DESTINY",
        )
        with pytest.raises(ValueError):
            key_builder.build(key, FIELD)
