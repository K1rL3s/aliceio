import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, cast

from aiohttp import JsonPayload, web
from aiohttp.abc import Application
from pydantic import BaseModel

from aliceio import Dispatcher, Skill
from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.types import Update
from aliceio.types.base import AliceObject
from aliceio.utils.funcs import build_json_payload

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class BaseAiohttpRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        **data: Any,
    ) -> None:
        """
        Базовый обработчик, который помогает обрабатывать входящий запрос от aiohttp
        и передавать его диспетчеру.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        :param json_loads: JSON Loads.
        :param json_dumps: JSON Dumps.
        """
        self.dispatcher = dispatcher
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.data = data
        # В идеале self.data должна передаваться в self.dispatcher.feed_webhook_update
        # как **kwargs, см. OneSkillAiohttpRequestHandler._handle_request

    def register(self, app: Application, /, path: str, **kwargs: Any) -> None:
        """
        Регистрирует эндпоинт и shutdown callback.

        :param app: Экземпляр aiohttp Application.
        :param path: Путь до эндпоинта.
        :param kwargs:
        """
        app.on_shutdown.append(self._handle_close)
        app.router.add_route("POST", path, self.handle, **kwargs)

    async def _handle_close(self, app: Application) -> None:
        await self.close()

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def resolve_skill(self, request: web.Request) -> Skill:
        """
        Этот метод должен быть реализован в наследниках этого класса.

        Получает экземпляр навыка из запроса.

        :param request:
        :return: Экземпляр навыка.
        """

    @abstractmethod
    async def _handle_request(
        self,
        skill: Skill,
        request: web.Request,
        update: Optional[Update] = None,
    ) -> web.Response:
        if update is None:
            update = await self._validate_update(skill, request)

        result = await self.dispatcher.feed_webhook_update(
            skill,
            update,
            **self.data,
        )
        return self._build_web_response(result)

    # Сделать здесь обработку, если прилетает некорректный update?
    async def _validate_update(self, skill: Skill, request: web.Request) -> Update:
        json_data = self._convert_show_pull_to_normal_request(
            await request.json(loads=self.json_loads),
        )
        return Update.model_validate(json_data, context={"skill": skill})

    async def handle(self, request: web.Request) -> web.Response:
        skill = await self.resolve_skill(request)
        return await self._handle_request(skill=skill, request=request)

    __call__ = handle

    # TODO: Проверить, помогает ли про запуске шоу Алисы
    @staticmethod
    def _convert_show_pull_to_normal_request(update: dict[str, Any]) -> dict[str, Any]:
        """
        При получении события запуска утреннего шоу вся информация
        (мета, сессия, версия и реквест) вероятно находится по ключу body.
        Эта функция выносит всю информацию за это поле.

        https://yandex.ru/dev/dialogs/alice/doc/ru/request-show-pull

        :param update:
        :return:
        """
        return cast(dict[str, Any], update.get("body", update))

    def _build_web_response(self, result: Any) -> web.Response:
        return web.Response(
            body=self._build_json_response(result=result),
            status=404 if result in (None, UNHANDLED, REJECTED) else 200,
        )

    def _build_json_response(self, result: Optional[AliceObject]) -> JsonPayload:
        return build_json_payload(
            value=result.model_dump() if isinstance(result, BaseModel) else result,
            json_dumps=self.json_dumps,
        )
