from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteSound, GetSounds, UploadSound
from aliceio.types import BufferedInputFile


class TestUploadImage:
    def test_api_url(self):
        method = UploadSound(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/sounds"


class TestGetSounds:
    def test_api_url(self):
        method = GetSounds(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/sounds"


class TestDeleteSound:
    def test_api_url(self):
        method = DeleteSound(file_id="FILE_ID")
        url = method.api_url(PRODUCTION, "SKILL")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/sounds/FILE_ID"
