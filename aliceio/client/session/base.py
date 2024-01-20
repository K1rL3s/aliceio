from __future__ import annotations

import abc
import datetime
import json
from enum import Enum
from http import HTTPStatus
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Dict, Final, Optional, Type, cast

from pydantic import ValidationError

from aliceio.exceptions import AliceAPIError, ClientDecodeError

from ...dispatcher.event.bases import REJECTED, UNHANDLED
from ...methods import AliceMethod, AliceType, ApiResponse
from ...types import ErrorResult, InputFile
from ..alice import PRODUCTION, AliceAPIServer
from .middlewares.manager import RequestMiddlewareManager

if TYPE_CHECKING:
    from ..skill import Skill

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
            raise ClientDecodeError("Failed to decode object", e, content)

        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
            try:
                response_type = ApiResponse[method.__returning__]  # type: ignore
                return response_type.model_validate(
                    json_data,
                    context={"skill": skill},
                )
            except ValidationError as e:
                raise ClientDecodeError("Failed to deserialize object", e, json_data)

        try:
            response = ErrorResult.model_validate(json_data)
        except ValidationError as e:
            raise ClientDecodeError("Failed to deserialize object", e, json_data)

        raise AliceAPIError(message=response.message)

    @abc.abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """Закрыть клиентскую сессию."""
        pass

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
        pass

    def prepare_value(  # noqa: C901
        self,
        value: Any,
        skill: Skill,
        files: Dict[str, Any],
        _dumps_json: bool = False,
    ) -> Any:
        """Подготовка значения перед отправкой."""
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if value in (UNHANDLED, REJECTED):
            return None
        if isinstance(value, InputFile):
            key = "file"
            files[key] = value
            return f"attach://{key}"
        if isinstance(value, dict):
            value = {
                key: prepared_item
                for key, item in value.items()
                if (
                    prepared_item := self.prepare_value(
                        item,
                        skill=skill,
                        files=files,
                        _dumps_json=False,
                    )
                )
                is not None
            }
            if _dumps_json:
                return self.json_dumps(value)
            return value
        if isinstance(value, list):
            value = [
                prepared_item
                for item in value
                if (
                    prepared_item := self.prepare_value(
                        item, skill=skill, files=files, _dumps_json=False
                    )
                )
                is not None
            ]
            if _dumps_json:
                return self.json_dumps(value)
            return value
        if isinstance(value, datetime.timedelta):
            now = datetime.datetime.now()
            return str(round((now + value).timestamp()))
        if isinstance(value, datetime.datetime):
            return str(round(value.timestamp()))
        if isinstance(value, Enum):
            return self.prepare_value(
                value.value, skill=skill, files=files, _dumps_json=True
            )

        if _dumps_json:
            return self.json_dumps(value)
        return value

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
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()
