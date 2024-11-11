from __future__ import annotations

import abc
import json
from http import HTTPStatus
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Final, Optional, cast

from pydantic import ValidationError

from aliceio.client.alice import PRODUCTION, AliceAPIServer
from aliceio.client.session.middlewares.manager import RequestMiddlewareManager
from aliceio.exceptions import AliceAPIError, ClientDecodeError
from aliceio.methods import AliceMethod, AliceType, ApiResponse
from aliceio.types import ErrorResult

if TYPE_CHECKING:
    from aliceio.client.skill import Skill

DEFAULT_TIMEOUT: Final[float] = 60.0
_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class BaseSession(abc.ABC):
    """
    Базовый класс для всех HTTP-сессий в aliceio.

    Если вы хотите создать свою собственную сессию, вы должны наследовать этот класс.
    """

    def __init__(
        self,
        api: AliceAPIServer = PRODUCTION,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """

        :param api: URL паттерны API Алисы.
        :param json_loads: JSON Loads.
        :param json_dumps: Json Dumps.
        :param timeout: Тайм-аут запроса сессии.
        """
        self.api = api
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.timeout = timeout

        self.middleware = RequestMiddlewareManager()

    def check_response(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
        status_code: int,
        content: str,
    ) -> ApiResponse[AliceType]:
        """Проверка статуса ответа."""
        try:
            json_data = self.json_loads(content)
        except Exception as e:
            # Обрабатываемая ошибка не может быть поймана конкретным типом,
            # поскольку декодер можно кастомизировать и вызвать любое исключение.
            raise ClientDecodeError("Failed to decode object", e, content) from e

        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
            try:
                response_type = ApiResponse[method.__returning__]  # type: ignore
                return response_type.model_validate(
                    {"result": json_data, "status_code": status_code},
                    context={"skill": skill},
                )
            except ValidationError as e:
                raise ClientDecodeError(
                    "Failed to deserialize object",
                    e,
                    json_data,
                ) from e

        try:
            response = ErrorResult.model_validate(json_data)
        except ValidationError as e:
            raise ClientDecodeError("Failed to deserialize object", e, json_data) from e

        raise AliceAPIError(message=response.message)

    @abc.abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """Закрыть клиентскую сессию."""

    @abc.abstractmethod
    async def make_request(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
        timeout: Optional[int] = None,
    ) -> AliceType:  # pragma: no cover
        """
        Запрос к API Алисы.

        :param skill: Навык.
        :param method: Метод.
        :param timeout: Таймаут.
        :return:
        :raise AliceApiError:
        """

    async def __call__(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
        timeout: Optional[int] = None,
    ) -> AliceType:
        middleware = self.middleware.wrap_middlewares(
            self.make_request,
            timeout=timeout,
        )
        return cast(AliceType, await middleware(skill, method))

    async def __aenter__(self) -> BaseSession:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()
