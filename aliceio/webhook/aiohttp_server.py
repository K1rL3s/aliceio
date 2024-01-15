from abc import ABC, abstractmethod
from asyncio import Transport
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, cast

from aiohttp import JsonPayload, web
from aiohttp.abc import Application
from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware

from aliceio import Dispatcher, Skill, loggers
from aliceio.types.base import AliceObject
from aliceio.webhook.security import IPFilter


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
                "Blocking request from an unauthorized IP: %s", ip_address
            )
            raise web.HTTPUnauthorized()
        return await handler(request)

    return _ip_filter_middleware


class BaseRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        **data: Any,
    ) -> None:
        """
        Базовый обработчик, который помогает обрабатывать входящий запрос от aiohttp
        и передавать его диспетчеру.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        :param handle_in_background: immediately responds to the Telegram instead of
            a waiting end of a handler process
        """
        self.dispatcher = dispatcher
        self.data = data

    def register(self, app: Application, /, path: str, **kwargs: Any) -> None:
        """
        Register route and shutdown callback

        :param app: instance of aiohttp Application
        :param path: route path
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
        This method should be implemented in subclasses of this class.

        Resolve Skill instance from request.

        :param request:
        :return: Skill instance
        """
        pass

    # TODO: Проверить, помогает ли про запуске шоу Алисы
    @staticmethod
    def _convert_show_pull_to_normal_request(update: Dict[str, Any]) -> Dict[str, Any]:
        """
        При получении события запуска утреннего шоу вся информация
        (мета, сессия, версия и реквест) находится по ключу body.
        Эта функция выносит всю информацию за это поле.

        :param update:
        :return:
        """
        return cast(Dict[str, Any], update.get("body", update))

    @staticmethod
    def _build_response_json(
        skill: Skill,
        result: Optional[AliceObject],
    ) -> JsonPayload:
        return JsonPayload(
            value=result.model_dump() if result else None,
        )

    async def _handle_request(self, skill: Skill, request: web.Request) -> web.Response:
        result = await self.dispatcher.feed_webhook_update(
            skill,
            await request.json(loads=skill.session.json_module.loads),
            **self.data,
        )
        return web.Response(body=self._build_response_json(skill=skill, result=result))

    async def handle(self, request: web.Request) -> web.Response:
        skill = await self.resolve_skill(request)
        return await self._handle_request(skill=skill, request=request)

    __call__ = handle


class OneSkillRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        skill: Skill,
        **data: Any,
    ) -> None:
        """
        Обработчик для одного экземпляра навыка.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        :param skill: Экземпляр :class:`aliceio.client.skill.Skill`
        """
        super().__init__(dispatcher=dispatcher, **data)
        self.skill = skill

    async def close(self) -> None:
        """Закрыть сессию навыка."""
        await self.skill.session.close()

    async def resolve_skill(self, request: web.Request) -> Skill:
        return self.skill
