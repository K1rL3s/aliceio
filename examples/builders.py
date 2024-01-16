import os
from typing import Any

from aiohttp import web

from aliceio import Dispatcher, F, Router, Skill
from aliceio.types import (
    AliceResponse,
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
from aliceio.webhook.aiohttp_server import OneSkillRequestHandler, setup_application

router = Router()

IMAGE_ID = "1030494/9cf43e52f64928daf818"


@router.message(F.command == "изображения")
async def items_list(message: Message) -> AliceResponse:
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
    ).add(ItemImage(image_id=IMAGE_ID, title="Четвёртая"))

    return AliceResponse(
        response=Response(
            text="Список айтемов",
            card=builder.to_collection(),
        )
    )


@router.message(F.command == "заголовок")
async def items_list_header_footer(message: Message) -> AliceResponse:
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

    return AliceResponse(
        response=Response(
            text="Список айтемов",
            card=builder.to_collection(),
        )
    )


@router.message(F.command == "галерея")
async def image_gallery(message: Message) -> AliceResponse:
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

    return AliceResponse(
        response=Response(
            text="Галерея изображений",
            card=builder.to_collection(),
        )
    )


@router.message(F.command == "кнопки")
async def text_buttons(message: Message) -> AliceResponse:
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

    return AliceResponse(
        response=Response(
            text="Обычные кнопочки",
            buttons=builder.to_collection(),
        )
    )


# Не обрабатывайте разные типы событий одной функцией
@router.button_pressed()
@router.message()
async def button_pressed(_: Any) -> AliceResponse:
    return AliceResponse(response=Response(text="Сомнительно, но окэй"))


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    skill_id = os.environ["SKILL_ID"]
    oauth_token = os.environ["OAUTH_TOKEN"]
    skill = Skill(
        skill_id=skill_id,
        oauth_token=oauth_token,
    )

    app = web.Application()
    webhook_requests_handler = OneSkillRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
