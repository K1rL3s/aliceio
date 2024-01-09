from typing import Any, Dict, Optional

import pytest

from aliceio.types import UploadedImage, UploadedSound


class TestUploadedImage:
    @pytest.mark.parametrize(
        "url,data",
        [
            [
                "https://test.org",
                {
                    "id": "42:IMAGE_ID",
                    "origUrl": "https://test.org",
                    "size": 1024,
                    "createdAt": "2000-01-01T12:00:00.000Z",
                },
            ],
            [
                None,
                {
                    "id": "42:IMAGE_ID",
                    "size": 1024,
                    "createdAt": "2000-01-01T12:00:00.000Z",
                },
            ],
        ],
    )
    def test_uploaded_image(
        self,
        url: Optional[str],
        data: Dict[str, Any],
    ) -> None:
        image = UploadedImage.model_validate(data)

        assert image.origUrl == image.orig_url == url
        assert image.createdAt == image.created_at


class TestUploadedSound:
    @pytest.mark.parametrize(
        "data",
        [
            {
                "id": "42:SOUND_ID",
                "skillId": "42:SKILL_ID",
                "size": 1024,
                "originalName": "dolphin-sound.mp3",
                "createdAt": "2000-01-01T12:00:00.000Z",
                "isProcessed": True,
                "error": None,
            },
            {
                "id": "42:SOUND_ID",
                "skillId": "42:SKILL_ID",
                "size": 1024,
                "originalName": "watermelon-sound.mp3",
                "createdAt": "2000-01-01T12:00:00.000Z",
                "isProcessed": False,
                "error": None,
            },
        ],
    )
    def test_uploaded_sound(self,data: Dict[str, Any]) -> None:
        sound = UploadedSound.model_validate(data)

        assert sound.createdAt == sound.created_at
        assert sound.skillId == sound.skill_id
        assert sound.originalName == sound.original_name
        assert sound.isProcessed == sound.is_processed
