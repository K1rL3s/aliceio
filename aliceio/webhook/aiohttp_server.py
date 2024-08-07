import json
from abc import ABC, abstractmethod
from asyncio import Transport
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, cast

from aiohttp import JsonPayload, web
from aiohttp.abc import Application
from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware
from pydantic import BaseModel

from aliceio import Dispatcher, Skill, loggers
from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.types import Update
from aliceio.types.base import AliceObject
from aliceio.utils.funcs import build_json_payload
from aliceio.webhook.security import IPFilter

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


def setup_application(
    app: Application,
    dispatcher: Dispatcher,
    /,
    **kwargs: Any,
) -> None:
    """
    Эта функция помогает настроить процесс запуска-выключения.

    :param app: aiohttp app
    :param dispatcher: aliceio dispatcher
    :param kwargs: additional data
    :return:
    """
    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*_: Any, **__: Any) -> None:  # pragma: no cover
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*_: Any, **__: Any) -> None:  # pragma: no cover
        await dispatcher.emit_shutdown(**workflow_data)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


def check_ip(ip_filter: IPFilter, request: web.Request) -> Tuple[str, bool]:
    # Попытка вычислить IP-адрес клиента после обратного прокси-сервера.
    if forwarded_for := request.headers.get("X-Forwarded-For", ""):
        # Получаем самый левый IP-адрес, если имеется несколько IP-адресов
        # (запрос получен через несколько прокси/балансировщиков нагрузки)
        forwarded_for, *_ = forwarded_for.split(",", maxsplit=1)
        return forwarded_for, forwarded_for in ip_filter

    # Если обратный прокси-сервер не настроен,
    # IP-адрес можно определить из входящего соединения.
    if peer_name := cast(Transport, request.transport).get_extra_info("peername"):
        host, _ = peer_name
        return host, host in ip_filter

    # Потенциально невозможный случай
    return "", False  # pragma: no cover


def ip_filter_middleware(
    ip_filter: IPFilter,
) -> Callable[[web.Request, Handler], Awaitable[Any]]:
    """

    :param ip_filter:
    :return:
    """

    @middleware
    async def _ip_filter_middleware(request: web.Request, handler: Handler) -> Any:
        ip_address, accept = check_ip(ip_filter=ip_filter, request=request)
        if not accept:
            loggers.webhook.warning(
                "Blocking request from an unauthorized IP: %s",
                ip_address,
            )
            raise web.HTTPUnauthorized
        return await handler(request)

    return _ip_filter_middleware


class BaseRequestHandler(ABC):
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
        # как **kwargs, см. OneSkillRequestHandler._handle_request

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
            update = cast(Update, self._update_validate(skill, request))

        result = await self.dispatcher.feed_webhook_update(
            skill,
            update,
            **self.data,
        )
        return self._build_web_response(result)

    # Сделать здесь обработку, если прилетает некорректный update?
    async def _update_validate(self, skill: Skill, request: web.Request) -> Update:
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
    def _convert_show_pull_to_normal_request(update: Dict[str, Any]) -> Dict[str, Any]:
        """
        При получении события запуска утреннего шоу вся информация
        (мета, сессия, версия и реквест) вероятно находится по ключу body.
        Эта функция выносит всю информацию за это поле.

        https://yandex.ru/dev/dialogs/alice/doc/ru/request-show-pull

        :param update:
        :return:
        """
        return cast(Dict[str, Any], update.get("body", update))

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


class OneSkillRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        skill: Skill,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        **data: Any,
    ) -> None:
        """
        Обработчик для одного экземпляра навыка.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        :param skill: Экземпляр :class:`aliceio.client.skill.Skill`
        """
        super().__init__(
            dispatcher=dispatcher,
            json_loads=json_loads,
            json_dumps=json_dumps,
            **data,
        )
        self.skill = skill

    async def close(self) -> None:
        """Закрыть сессию навыка."""
        await self.skill.session.close()

    async def resolve_skill(self, request: web.Request) -> Skill:
        return self.skill

    async def _handle_request(
        self,
        skill: Skill,
        request: web.Request,
        update: Optional[Update] = None,
    ) -> web.Response:
        update = await self._update_validate(skill, request)

        # Проверка айди навыка в поступившем событии
        if update.session.skill_id != skill.skill_id:
            loggers.webhook.warning(
                "Update came from a skill id=%r, but was expected skill id=%r",
                update.session.skill_id,
                skill.skill_id,
            )
            return web.Response(body="Not Acceptable", status=406)

        return await super()._handle_request(skill, request, update)
