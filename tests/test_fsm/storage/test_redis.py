from typing import Final, Optional

import pytest

from aliceio.fsm.storage.base import DEFAULT_DESTINY, StorageKey
from aliceio.fsm.storage.redis import DefaultKeyBuilder

PREFIX = "test"
SKILL_ID = "42:SKILL_ID"
USER_ID = "42:USER_ID"
SESSION_ID = "42:SESSION_ID"
APPLICATION_ID = "42:APP_ID"
FIELD: Final = "data"


class TestRedisDefaultKeyBuilder:
    @pytest.mark.parametrize(
        "skill_id,user_id,session_id,application_id,with_destiny,result",
        [
            [
                SKILL_ID,
                USER_ID,
                SESSION_ID,
                APPLICATION_ID,
                True,
                f"{PREFIX}:{SKILL_ID}:{USER_ID}:{SESSION_ID}:{APPLICATION_ID}:{DEFAULT_DESTINY}:{FIELD}",
            ],
            [
                SKILL_ID,
                None,
                None,
                None,
                False,
                f"{PREFIX}:{SKILL_ID}::::{FIELD}",
            ],
            [
                SKILL_ID,
                None,
                None,
                None,
                True,
                f"{PREFIX}:{SKILL_ID}::::{DEFAULT_DESTINY}:{FIELD}",
            ],
        ],
    )
    async def test_generate_key(
        self,
        skill_id: str,
        user_id: Optional[str],
        session_id: Optional[str],
        application_id: Optional[str],
        with_destiny: bool,
        result: str,
    ) -> None:
        key_builder = DefaultKeyBuilder(
            prefix=PREFIX,
            with_destiny=with_destiny,
        )
        key = StorageKey(
            skill_id=skill_id,
            user_id=user_id,
            session_id=session_id,
            application_id=application_id,
            destiny=DEFAULT_DESTINY,
        )
        assert key_builder.build(key, FIELD) == result

    async def test_destiny_check(self) -> None:
        key_builder = DefaultKeyBuilder(with_destiny=False)
        key = StorageKey(
            skill_id=SKILL_ID,
            user_id=USER_ID,
            session_id=SESSION_ID,
            application_id=APPLICATION_ID,
        )
        assert key_builder.build(key, FIELD)

        key = StorageKey(
            skill_id=SKILL_ID,
            user_id=USER_ID,
            session_id=SESSION_ID,
            application_id=APPLICATION_ID,
            destiny="CUSTOM_TEST_DESTINY",
        )
        with pytest.raises(ValueError):
            key_builder.build(key, FIELD)
