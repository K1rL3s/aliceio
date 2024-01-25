from aliceio.enums import EventType
from aliceio.types import TimeoutUpdate, Update


class TestTimeoutUpdate:
    def test_event(self, update: Update):
        event = TimeoutUpdate.model_validate(
            update.model_dump(),
            context={"skill": update.skill},
        )

        assert event.event_type == EventType.TIMEOUT
        assert event._real_event_type == update.event_type

        assert isinstance(event.event, type(update.event))
        assert event.event == update.event

        assert event.skill == update.skill
        assert event.skill is update.skill
