from aliceio.types import TimeoutEvent, Update


class TestTimeoutEvent:
    def test_event(self, update: Update):
        event = TimeoutEvent(update=update, session=update.session)
        assert event.event == update.event
