import pytest

from aliceio.client.alice import PRODUCTION
from aliceio.exceptions import AliceWrongFieldError
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
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL_ID/images"

    def test_fields_not_empty(self):
        with pytest.raises(AliceWrongFieldError):
            UploadImage()
        with pytest.raises(AliceWrongFieldError):
            UploadImage(file=BufferedInputFile(file=b""), url="url")

        UploadImage(file=BufferedInputFile(file=b""))
        UploadImage(url="url")


class TestGetImages:
    def test_api_url(self, skill: MockedSkill):
        method = GetImages(file=BufferedInputFile(file=b""))

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL_ID/images"


class TestDeleteImage:
    def test_api_url(self, skill: MockedSkill):
        method = DeleteImage(file_id="FILE_ID")

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert (
            url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL_ID/images/FILE_ID"
        )
