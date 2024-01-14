from aliceio.client.alice import PRODUCTION
from aliceio.methods import Status


class TestStatusMethod:
    def test_response_validate(self):
        method = Status()
        data = {
            "images": {"quota": {"total": 1000, "used": 100}},
            "sounds": {"quota": {"total": 2000, "used": 200}},
        }

        space = method.response_validate(data)

        assert space.images.total == 1000
        assert space.images.used == 100
        assert space.images.available == 900

        assert space.sounds.total == 2000
        assert space.sounds.used == 200
        assert space.sounds.available == 1800

    def test_api_url(self):
        method = Status()
        url = method.api_url(PRODUCTION, "42:SKILL")

        assert url == "https://dialogs.yandex.net/api/v1/status"
