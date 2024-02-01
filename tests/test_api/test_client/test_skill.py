from unittest.mock import AsyncMock, patch

import pytest

from aliceio import Skill
from aliceio.client.session.aiohttp import AiohttpSession
from aliceio.methods import (
    DeleteImage,
    DeleteSound,
    GetImages,
    GetSounds,
    Status,
    UploadImage,
    UploadSound,
)
from aliceio.types import (
    BufferedInputFile,
    PreQuota,
    PreUploadedImage,
    PreUploadedSound,
    Quota,
    Result,
    SpaceStatus,
    UploadedImage,
    UploadedImagesList,
    UploadedSound,
    UploadedSoundsList,
)
from tests.mocked import MockedSkill


class TestSkill:
    @pytest.mark.parametrize(
        "token",
        ["42:OAUTH", None, 42],
    )
    def test_oauth_token_getters(self, token):
        skill = Skill(skill_id="42:SKILL_ID", oauth_token=token)

        assert skill.token == skill.oauth_token == token

    @pytest.mark.parametrize(
        "skill_id",
        ["42:SKILL_ID", None, 42],
    )
    def test_skill_id_getters(self, skill_id):
        skill = Skill(skill_id=skill_id)

        assert skill.id == skill.skill_id == skill_id

    async def test_context_manager(self):
        skill = Skill(skill_id="42:SKILL_ID", oauth_token="42:OAUTH")

        assert isinstance(skill.session, AiohttpSession)
        await skill.session.create_session()

        async with skill.context(auto_close=False) as contexted_skill:
            assert skill is contexted_skill
        assert not skill.session._session.closed

        async with skill.context(auto_close=True) as contexted_skill:
            assert skill is contexted_skill
        assert skill.session._session.closed

    def test_equal(self):
        skill_1 = Skill(skill_id="1")
        skill_2 = Skill(skill_id="1")
        skill_3 = Skill(skill_id="2")
        smt = 42

        assert skill_1 == skill_2
        assert skill_1 != skill_3
        assert skill_2 != skill_3
        assert skill_1 != smt
        assert skill_2 != smt
        assert skill_3 != smt

    async def test_status(self, skill: MockedSkill):
        skill.add_result_for(
            Status,
            result=SpaceStatus(
                images=PreQuota(quota=Quota(total=1000, used=100)),
                sounds=PreQuota(quota=Quota(total=2000, used=200)),
            ),
        )
        space_status = await skill.status()

        assert space_status.images.quota.total == 1000
        assert space_status.images.quota.used == 100
        assert space_status.images.quota.available == 900
        assert space_status.sounds.quota.total == 2000
        assert space_status.sounds.quota.used == 200
        assert space_status.sounds.quota.available == 1800

    async def test_get_images(self, skill: MockedSkill):
        skill.add_result_for(
            GetImages,
            result=UploadedImagesList(
                images=[
                    UploadedImage(id="id1", size=100, createdAt="1"),
                    UploadedImage(id="id2", size=200, createdAt="2", origUrl="url"),
                ],
            ),
        )
        images = await skill.get_images()

        assert isinstance(images, UploadedImagesList)
        assert len(images.images) == 2
        assert images.images[0].id == "id1"
        assert images.images[0].size == 100
        assert images.images[0].origUrl is None
        assert images.images[0].createdAt == "1"

        assert images.images[1].id == "id2"
        assert images.images[1].size == 200
        assert images.images[1].origUrl == "url"
        assert images.images[1].createdAt == "2"

    async def test_upload_image(self, skill: MockedSkill):
        skill.add_result_for(
            UploadImage,
            result=PreUploadedImage(
                image=UploadedImage(id="id1", size=100, createdAt="1")
            ),
        )
        image = await skill.upload_image(BufferedInputFile(b""))

        assert isinstance(image, PreUploadedImage)
        assert image.image.id == "id1"
        assert image.image.size == 100
        assert image.image.origUrl is None
        assert image.image.createdAt == "1"

    async def test_upload_image_overload_str(self, skill: MockedSkill):
        with patch(
            "aliceio.client.skill.Skill.__call__",
            new_callable=AsyncMock,
        ) as mock:
            await skill.upload_image("url")
            upload = mock.await_args_list[0][0][0]

            assert isinstance(upload, UploadImage)
            assert upload.file is None
            assert upload.url == "url"

    async def test_upload_image_overload_file(self, skill: MockedSkill):
        with patch(
            "aliceio.client.skill.Skill.__call__",
            new_callable=AsyncMock,
        ) as mock:
            await skill.upload_image(BufferedInputFile(file=b"\f" * 10, chunk_size=10))
            upload = mock.await_args_list[0][0][0]

            async for chunk in upload.file.read():
                assert chunk == b"\f" * 10
            assert isinstance(upload, UploadImage)
            assert upload.url is None

    async def test_delete_image(self, skill: MockedSkill):
        skill.add_result_for(DeleteImage, result=Result(result="ok"))
        result = await skill.delete_image("id")

        assert isinstance(result, Result)
        assert result.result == "ok"

    async def test_get_sounds(self, skill: MockedSkill):
        skill.add_result_for(
            GetSounds,
            result=UploadedSoundsList(
                sounds=[
                    UploadedSound(
                        id="id1",
                        skillId=skill.id,
                        size=100,
                        originalName="n1",
                        createdAt="c1",
                        isProcessed=True,
                    ),
                    UploadedSound(
                        id="id2",
                        skillId=skill.id,
                        size=200,
                        originalName="n2",
                        createdAt="c2",
                        isProcessed=False,
                    ),
                ],
            ),
        )
        sounds = await skill.get_sounds()

        assert isinstance(sounds, UploadedSoundsList)
        assert len(sounds.sounds) == 2

        assert sounds.sounds[0].id == "id1"
        assert sounds.sounds[0].skillId == skill.id
        assert sounds.sounds[0].size == 100
        assert sounds.sounds[0].originalName == "n1"
        assert sounds.sounds[0].createdAt == "c1"
        assert sounds.sounds[0].isProcessed is True

        assert sounds.sounds[1].id == "id2"
        assert sounds.sounds[1].skillId == skill.id
        assert sounds.sounds[1].size == 200
        assert sounds.sounds[1].originalName == "n2"
        assert sounds.sounds[1].createdAt == "c2"
        assert sounds.sounds[1].isProcessed is False

    async def test_upload_sound(self, skill: MockedSkill):
        skill.add_result_for(
            UploadSound,
            result=PreUploadedSound(
                sound=UploadedSound(
                    id="id1",
                    skillId=skill.id,
                    size=100,
                    originalName="n1",
                    createdAt="c1",
                    isProcessed=True,
                ),
            ),
        )
        sound = await skill.upload_sound(BufferedInputFile(b""))

        assert isinstance(sound, PreUploadedSound)
        assert sound.sound.id == "id1"
        assert sound.sound.skillId == skill.id
        assert sound.sound.size == 100
        assert sound.sound.originalName == "n1"
        assert sound.sound.createdAt == "c1"
        assert sound.sound.isProcessed is True

    async def test_delete_sound(self, skill: MockedSkill):
        skill.add_result_for(DeleteSound, result=Result(result="ok"))
        result = await skill.delete_sound("id")

        assert result.result == "ok"
