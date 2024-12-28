"""
Кнопочки

https://yandex.ru/dev/dialogs/alice/doc/ru/buttons
"""

import logging
import os
import sys
from typing import Any

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.types import (
    ImageGalleryItem,
    ItemImage,
    MediaButton,
    Message,
    Response,
    TextButton,
)
from aliceio.utils.builders import (
    ImageGalleryBuilder,
    ItemsListBuilder,
    TextButtonsBuilder,
)
from aliceio.webhook.aiohttp_server import (
    OneSkillAiohttpRequestHandler,
    setup_application,
)

router = Router()

IMAGE_ID = "1030494/9cf43e52f64928daf818"  # вставьте своё любое айди картинки


@router.message(F.command == "изображения")
async def items_list(message: Message) -> Response:
    builder = ItemsListBuilder()
    builder.add(
        IMAGE_ID,
        title="Первая",
    ).add(
        IMAGE_ID,
        description="Описание",
    ).add(
        IMAGE_ID,
        button=MediaButton(text="3.5", url="https://ya.ru"),
    ).add(
        ItemImage(image_id=IMAGE_ID, title="Четвёртая"),
    )

    return Response(
        text="Список айтемов",
        card=builder.to_collection(),
    )


@router.message(F.command == "заголовок")
async def items_list_header_footer(message: Message) -> Response:
    builder = ItemsListBuilder()
    builder.add(
        IMAGE_ID,
        title="Первая",
    ).add(
        IMAGE_ID,
        title="Вторая",
    )
    builder.set_header(
        "Хеадер сообщения",
    ).set_footer(
        "Футер сообщения",
        button=MediaButton(text="Кнопка", url="https://ya.ru"),
    )

    # Ещё один возможный способ:
    # builder.set_header(CardHeader(text="Хеадер сообщения")).set_footer(
    #     CardFooter(
    #         text="Футер сообщения",
    #         button=MediaButton(text="Кнопка", url="https://ya.ru"),
    #     )
    # )

    return Response(
        text="Список айтемов",
        card=builder.to_collection(),
    )


@router.message(F.command == "галерея")
async def image_gallery(message: Message) -> Response:
    builder = ImageGalleryBuilder()
    builder.add(
        IMAGE_ID,
    ).add(
        IMAGE_ID,
        title="Заголовок",
    ).add(
        IMAGE_ID,
        button=MediaButton(text="3.5", url="https://ya.ru"),
    ).add(
        ImageGalleryItem(image_id=IMAGE_ID, title="4"),
    )

    return Response(
        text="Галерея изображений",
        card=builder.to_collection(),
    )


@router.message(F.command == "кнопки")
async def text_buttons(message: Message) -> Response:
    builder = TextButtonsBuilder()
    builder.add(
        "Первая",
    ).add(
        "Вторая",
        url="https://ya.ru",
    ).add(
        "Третья",
        payload={"k": "v"},
    ).add(
        "Четвёртая",
        hide=False,
    ).add(
        TextButton(title="Пятая"),
    )

    return Response(
        text="Обычные кнопочки",
        buttons=builder.to_collection(),
    )


# Не обрабатывайте разные типы событий одной функцией, это ради примера
@router.button_pressed()
@router.message()
async def button_pressed(_: Any) -> Response:
    return Response(text="Сомнительно, но окэй")


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    skill_id = os.environ["SKILL_ID"]
    skill = Skill(skill_id=skill_id)

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
