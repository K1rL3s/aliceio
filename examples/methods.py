"""
Добавление аудио, изображений и проверка доступного места

https://yandex.ru/dev/dialogs/alice/doc/ru/resource-upload
https://yandex.ru/dev/dialogs/alice/doc/ru/resource-sounds-upload
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

from aiohttp import web

from aliceio import Dispatcher, F, Skill
from aliceio.types import BufferedInputFile, FSInputFile, Message, Response
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

# Для использования методов API Алисы обязательно нужен oauth token!
dp = Dispatcher()
DATA_DIR = Path(__file__).parent / "data"


@dp.message(F.command == "статус")
async def status(message: Message, skill: Skill) -> Response:
    space_status = await skill.status()
    return Response(text=str(space_status))


@dp.message(F.command == "загрузи фото")
async def upload_photo(message: Message, skill: Skill) -> Response:
    with open(DATA_DIR / "watermelon.png", "rb") as f:
        image = BufferedInputFile(file=f.read())
    picture = FSInputFile(path=DATA_DIR / "watermelon.png")
    url = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/"
        "Yandex_Logo.svg/2560px-Yandex_Logo.svg.png"
    )

    tasks = [
        skill.upload_image(image),
        skill.upload_image(picture),
        skill.upload_image(url),
    ]
    results = await asyncio.gather(*tasks)

    return Response(text=str(results))


@dp.message(F.command == "загрузи аудио")
async def upload_sounds(message: Message, skill: Skill) -> Response:
    with open(DATA_DIR / "watermelon_rip.mp3", "rb") as f:
        audio = BufferedInputFile(file=f.read())
    sound = FSInputFile(path=DATA_DIR / "watermelon_rip2.mp3")

    tasks = [
        skill.upload_sound(audio),
        skill.upload_sound(sound),
    ]
    results = await asyncio.gather(*tasks)

    return Response(text=str(results))


@dp.message(F.command == "все фото")
async def get_all_images(message: Message, skill: Skill) -> Response:
    pre_images = await skill.get_images()
    images = pre_images.images
    return Response(text=str(images))


@dp.message(F.command == "все аудио")
async def get_all_sounds(message: Message, skill: Skill) -> Response:
    pre_sounds = await skill.get_sounds()
    sounds = pre_sounds.sounds
    return Response(text=str(sounds))


@dp.message(F.command == "удали фото")
async def delete_image(message: Message, skill: Skill) -> Response:
    images = (await skill.get_images()).images
    if images:
        image = images[0]
        result = await skill.delete_image(image.id)
        text = f"Удалил это изображение ({result}):\n{image}"
    else:
        text = "Нет изображений, которые можно удалить"
    return Response(text=text)


@dp.message(F.command == "удали аудио")
async def delete_sound(message: Message, skill: Skill) -> Response:
    sounds = (await skill.get_sounds()).sounds
    if sounds:
        sound = sounds[0]
        result = await skill.delete_sound(sound.id)
        text = f"Удалил это аудио ({result}):\n{sound}"
    else:
        text = "Нет аудио, которые можно удалить"
    return Response(text=text)


@dp.message()
async def any_message(message: Message) -> Response:
    return Response(text="Привет!")


def main() -> None:
    # ouath_token обязателен!
    skill_id = os.environ["SKILL_ID"]
    oauth_token = os.environ["OAUTH_TOKEN"]
    skill = Skill(
        skill_id=skill_id,
        oauth_token=oauth_token,
    )

    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(dispatcher=dp, skill=skill)

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
