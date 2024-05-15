import logging

from aliceio.client.session.middlewares.request_logging import RequestLogging
from aliceio.methods import GetImages, Status
from aliceio.types import (
    PreQuota,
    Quota,
    SpaceStatus,
    UploadedImage,
    UploadedImagesList,
)
from tests.mocked.mocked_skill import MockedSkill


class TestRequestLogging:
    async def test_use_middleware(self, skill: MockedSkill, caplog):
        caplog.set_level(logging.INFO)
        skill.session.middleware(RequestLogging())

        skill.add_result_for(
            Status,
            result=SpaceStatus(
                images=PreQuota(quota=Quota(total=1000, used=100)),
                sounds=PreQuota(quota=Quota(total=2000, used=200)),
            ),
        )
        assert await skill.status()
        assert (
            "Make request with method='Status' by skill id='42:SKILL_ID'" in caplog.text
        )

    async def test_ignore_methods(self, skill: MockedSkill, caplog):
        caplog.set_level(logging.INFO)
        skill.session.middleware(RequestLogging(ignore_methods=[Status]))

        skill.add_result_for(
            Status,
            result=SpaceStatus(
                images=PreQuota(quota=Quota(total=1000, used=100)),
                sounds=PreQuota(quota=Quota(total=2000, used=200)),
            ),
        )
        assert await skill.status()
        assert (
            "Make request with method='Status' by skill id='42:SKILL_ID'"
            not in caplog.text
        )

        skill.add_result_for(
            GetImages,
            result=UploadedImagesList(
                images=[
                    UploadedImage(
                        id="42:IMAGE",
                        size=100,
                        createdAt="date",
                    ),
                ],
            ),
        )
        assert await skill.get_images()
        assert (
            "Make request with method='GetImages' by skill id='42:SKILL_ID'"
            in caplog.text
        )
