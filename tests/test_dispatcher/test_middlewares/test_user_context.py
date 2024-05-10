from unittest.mock import patch

import pytest

from aliceio.dispatcher.middlewares.user_context import UserContextMiddleware
from aliceio.types import Application, TimeoutUpdate, Update, User
from tests.mocked import create_mocked_session, create_mocked_update


async def next_handler(*args, **kwargs):
    pass


class TestUserContextMiddleware:
    async def test_unexpected_event_type(self):
        with pytest.raises(RuntimeError):
            await UserContextMiddleware()(next_handler, None, {})

    async def test_expected_event_type(self, update: Update):
        timeout = TimeoutUpdate.model_validate(update, from_attributes=True)
        await UserContextMiddleware()(next_handler, update, {})
        await UserContextMiddleware()(next_handler, timeout, {})

    async def test_call(self, update: Update) -> None:
        middleware = UserContextMiddleware()
        data = {}
        with patch.object(
            UserContextMiddleware,
            "resolve_event_context",
            return_value=[1, 2],
        ):
            await middleware(next_handler, update, data)

        assert data["event_session"] == 1
        assert data["event_from_user"] == 2
        assert data["event_update"] == update

        data.clear()
        await middleware(next_handler, update, data)

        assert data["event_session"] == update.session
        assert data["event_from_user"] == update.session.user
        assert data["event_update"] == update

    async def test_resolve_context(self) -> None:
        user = User(user_id="42", access_token="24")
        application = Application(application_id="123")
        session = create_mocked_session(user=user, application=application)
        update = create_mocked_update(session=session)

        middleware = UserContextMiddleware()
        data = {}
        await middleware(next_handler, update, data)

        assert data["event_session"] == session
        assert data["event_from_user"] == user
