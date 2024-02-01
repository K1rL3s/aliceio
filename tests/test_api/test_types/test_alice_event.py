import pytest

from aliceio.types.alice_event import AliceEvent
from tests.mocked import create_mocked_update


class TestAliceEvent:
    @pytest.mark.parametrize("event", [create_mocked_update().event])
    def test_alice_event(self, event: AliceEvent) -> None:
        assert event.from_user == event.user
