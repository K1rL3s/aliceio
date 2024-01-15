import pytest

from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteSound, GetSounds, UploadSound
from aliceio.types import BufferedInputFile
from tests.mocked import MockedSkill


class TestUploadImage:
    def test_api_url(self, skill: MockedSkill):
        method = UploadSound(file=BufferedInputFile(file=b""))

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/sounds"


class TestGetSounds:
    def test_api_url(self, skill: MockedSkill):
        method = GetSounds(file=BufferedInputFile(file=b""))

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/sounds"


class TestDeleteSound:
    def test_api_url(self, skill: MockedSkill):
        method = DeleteSound(file_id="FILE_ID")

        with pytest.raises(AttributeError):
            method.api_url(PRODUCTION)

        method.as_(skill)
        url = method.api_url(PRODUCTION)
        assert url == "https://dialogs.yandex.net/api/v1/skills/42:SKILL/sounds/FILE_ID"
