"""Generated by AI :("""

import time
import uuid

from aiohttp import web

# Конфигурация OAuth приложения
REDIRECT_URI = "https://social.yandex.net/broker/redirect"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

# Временное хранилище для кодов авторизации и токенов
auth_codes = {}
access_tokens = {}


async def authorize_endpoint(request: web.Request) -> web.Response:
    # Проверка обязательных параметров
    params = request.rel_url.query
    response_type = params.get("response_type")
    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")

    if (
        response_type != "code"
        or client_id != CLIENT_ID
        or redirect_uri != REDIRECT_URI
    ):
        return web.Response(text="Invalid request", status=400)

    # Генерация и сохранение авторизационного кода
    code = str(uuid.uuid4())
    auth_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "expires_at": time.time() + 600,  # Код авторизации действителен 10 минут
    }

    # Перенаправление пользователя на redirect_uri с авторизационным кодом
    return web.HTTPFound(f"{redirect_uri}?code={code}&state={params.get('state')}")


async def token_endpoint(request: web.Request) -> web.Response:
    data = await request.post()
    grant_type = data.get("grant_type")
    code = data.get("code")
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")

    # Проверка обязательных параметров и валидности кода
    if (
        grant_type != "authorization_code"
        or client_id != CLIENT_ID
        or client_secret != CLIENT_SECRET
    ):
        return web.Response(text="Invalid request", status=400)

    if code not in auth_codes or auth_codes[code]["client_id"] != client_id:
        return web.Response(text="Invalid code", status=400)

    access_token = str(uuid.uuid4())
    refresh_token = str(uuid.uuid4())
    expires_in = 3600  # Время жизни токена, в секундах (1 час)

    access_tokens[access_token] = {
        "client_id": client_id,
        "expires_at": time.time() + expires_in,
    }

    del auth_codes[code]

    return web.json_response(
        {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": expires_in,
            "refresh_token": refresh_token,
        },
    )
