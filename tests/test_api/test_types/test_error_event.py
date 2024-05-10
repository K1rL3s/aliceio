from aliceio.types import ErrorEvent, Update


class TestErrorEvent:
    def test_event(self, update: Update):
        event = ErrorEvent(
            update=update,
            exception=KeyError("KABOOM"),
            session=update.session,
        )
        assert event.event == update.event
