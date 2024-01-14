from aliceio.client.alice import PRODUCTION
from aliceio.methods import DeleteImage, GetImages, UploadImage
from aliceio.types import BufferedInputFile, UploadedImage


class TestUploadImage:
    def test_response_validate(self):
        method = UploadImage(file=BufferedInputFile(file=b""))
        data = {
            "image": {
                "id": "FILE_ID",
                "origUrl": None,
                "size": 1000,
                "createdAt": "2024-01-01T00:00:00.000Z",
            }
        }

        result = method.response_validate(data)

        assert isinstance(result, UploadedImage)
        assert result.id == "FILE_ID"
        assert result.origUrl is result.orig_url is None
        assert result.size == 1000
        assert result.createdAt == result.created_at == "2024-01-01T00:00:00.000Z"

    def test_api_url(self):
        method = UploadImage(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images"


class TestGetImages:
    def test_response_validate(self):
        method = GetImages()
        data = {
            "images": [
                {
                    "id": "FILE_1",
                    "origUrl": None,
                    "size": 1000,
                    "createdAt": "2024-01-01T00:00:00.000Z",
                },
                {
                    "id": "FILE_2",
                    "origUrl": "http://example.com",
                    "size": 2000,
                    "createdAt": "2023-12-31T00:00:00.000Z",
                },
            ]
        }

        result = method.response_validate(data)

        assert isinstance(result, list)
        im1, im2 = result[0], result[1]

        assert im1.id == "FILE_1"
        assert im1.origUrl is im1.orig_url is None
        assert im1.size == 1000
        assert im1.createdAt == im1.created_at == "2024-01-01T00:00:00.000Z"

        assert im2.id == "FILE_2"
        assert im2.origUrl == im2.orig_url == "http://example.com"
        assert im2.size == 2000
        assert im2.createdAt == im2.created_at == "2023-12-31T00:00:00.000Z"

    def test_api_url(self):
        method = GetImages(file=BufferedInputFile(file=b""))
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images"


class TestDeleteImage:
    def test_response_validate(self):
        method = DeleteImage(file_id="FILE_ID")
        data = {"result": "ok"}

        result = method.response_validate(data)

        assert result.result == "ok"

    def test_api_url(self):
        method = DeleteImage(file_id="FILE_ID")
        url = method.api_url(PRODUCTION, "SKILL_ID")

        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL_ID/images/FILE_ID"
