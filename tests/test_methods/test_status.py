from aliceio.client.alice import PRODUCTION
from aliceio.methods import Status
from tests.mocked import MockedSkill


class TestStatusMethod:
    def test_api_url(self, skill: MockedSkill):
        method = Status()

        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/status"

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/status"
