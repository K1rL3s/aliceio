import pytest

from aliceio.types import Application, Session, User


class TestSession:
    @pytest.mark.parametrize(
        "user,is_anonymous",
        [
            [User(user_id="42:USER_ID", access_token="42:ACCESS_TOKEN"), False],
            [None, True],
        ],
    )
    def test_is_anonymous(self, user: User, is_anonymous: bool):
        session = Session(
            message_id=0,
            session_id="42:SESSION_ID",
            skill_id="42:SKILL_ID",
            user=user,
            application=Application(application_id="42:APP_ID"),
            new=False,
        )
        assert session.is_anonymous is is_anonymous
