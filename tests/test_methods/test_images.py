import pytest

from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteImage, GetImages, UploadImage
from aliceio.types import BufferedInputFile
from tests.mocked import MockedSkill


class TestUploadImage:
    def test_api_url(self, skill: MockedSkill):
        method = UploadImage(file=BufferedInputFile(file=b""))

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/images"


class TestGetImages:
    def test_api_url(self, skill: MockedSkill):
        method = GetImages(file=BufferedInputFile(file=b""))

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/images"


class TestDeleteImage:
    def test_api_url(self, skill: MockedSkill):
        method = DeleteImage(file_id="FILE_ID")

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/images/FILE_ID"
