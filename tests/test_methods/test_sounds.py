from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteSound, GetSounds, UploadSound
from aliceio.types import BufferedInputFile, UploadedSound


class TestUploadImage:
    def test_response_validate(self):
        method = UploadSound(file=BufferedInputFile(file=b""))
        data = {
            "sound": {
                "id": "FILE_ID",
                "skillId": "SKILL_ID",
                "size": 1000,
                "originalName": "watermelon_rip1.mp3",
                "createdAt": "2024-01-01T00:00:00.000Z",
                "isProcessed": True,
                "error": None,
            }
        }

        result = method.response_validate(data)

        assert isinstance(result, UploadedSound)
        assert result.id == "FILE_ID"
        assert result.skillId == result.skill_id == "SKILL_ID"
        assert result.size == 1000
        assert result.originalName == result.original_name == "watermelon_rip1.mp3"
        assert result.createdAt == result.created_at == "2024-01-01T00:00:00.000Z"
        assert result.isProcessed is result.is_processed is True
        assert result.error is None

    def test_api_url(self):
        method = UploadSound(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/sounds"


class TestGetSounds:
    def test_response_validate(self):
        method = GetSounds()
        data = {
            "sounds": [
                {
                    "id": "FILE_1",
                    "skillId": "SKILL_ID",
                    "size": 1000,
                    "originalName": "watermelon_rip1.mp3",
                    "createdAt": "2024-01-01T00:00:00.000Z",
                    "isProcessed": True,
                    "error": None,
                },
                {
                    "id": "FILE_2",
                    "skillId": "SKILL_ID",
                    "size": 2000,
                    "originalName": "watermelon_rip2.mp3",
                    "createdAt": "2023-12-31T00:00:00.000Z",
                    "isProcessed": True,
                    "error": None,
                },
            ]
        }

        result = method.response_validate(data)

        assert isinstance(result, list)
        sound1, sound2 = result[0], result[1]

        assert isinstance(sound1, UploadedSound)
        assert sound1.id == "FILE_1"
        assert sound1.skillId == sound1.skill_id == "SKILL_ID"
        assert sound1.size == 1000
        assert sound1.originalName == sound1.original_name == "watermelon_rip1.mp3"
        assert sound1.createdAt == sound1.created_at == "2024-01-01T00:00:00.000Z"
        assert sound1.isProcessed is sound1.is_processed is True
        assert sound1.error is None

        assert isinstance(sound2, UploadedSound)
        assert sound2.id == "FILE_2"
        assert sound2.skillId == sound2.skill_id == "SKILL_ID"
        assert sound2.size == 2000
        assert sound2.originalName == sound2.original_name == "watermelon_rip2.mp3"
        assert sound2.createdAt == sound2.created_at == "2023-12-31T00:00:00.000Z"
        assert sound2.isProcessed is sound2.is_processed is True
        assert sound2.error is None

    def test_api_url(self):
        method = GetSounds(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/sounds"


class TestDeleteSound:
    def test_response_validate(self):
        method = DeleteSound(file_id="FILE_ID")
        data = {"result": "ok"}

        result = method.response_validate(data)

        assert result.result == "ok"

    def test_api_url(self):
        method = DeleteSound(file_id="FILE_ID")
        url = method.api_url(PRODUCTION, "SKILL")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/sounds/FILE_ID"
