from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteImage, GetImages, UploadImage
from aliceio.types import BufferedInputFile


class TestUploadImage:
    def test_api_url(self):
        method = UploadImage(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images"


class TestGetImages:
    def test_api_url(self):
        method = GetImages(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images"


class TestDeleteImage:
    def test_api_url(self):
        method = DeleteImage(file_id="FILE_ID")
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images/FILE_ID"
