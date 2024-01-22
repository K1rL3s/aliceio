from aliceio.types import TimeoutUpdate, Update


class TestTimeoutEvent:
    def test_event(self, update: Update):
        event = TimeoutUpdate.model_validate(
            update.model_dump(),
            context={"skill": update.skill},
        )
        assert event.event == update.event
        assert event.skill == update.skill
