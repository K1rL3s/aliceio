from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from aliceio.methods import AliceMethod, Response
from aliceio.methods.base import AliceType

if TYPE_CHECKING:
    from ...skill import Skill


class NextRequestMiddlewareType(Protocol[AliceType]):  # pragma: no cover
    async def __call__(
        self,
        skill: "Skill",
        method: AliceMethod[AliceType],
    ) -> Response[AliceType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[AliceType],
        skill: "Skill",
        method: AliceMethod[AliceType],
    ) -> Response[AliceType]:
        pass


class BaseRequestMiddleware(ABC):
    """Базовый дженерик мидлварь"""

    @abstractmethod
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[AliceType],
        skill: "Skill",
        method: AliceMethod[AliceType],
    ) -> Response[AliceType]:
        """
        Вызов мидлваря.

        :param make_request: Обёрнутый make_request в цепочке мидлварей.
        :param skill: Бот для выполнения запросов
        :param method: Метод запроса
                       (Подкласс :class:`aiolice.methods.base.AliceMethod`)

        :return: :class:`aiolice.methods.Response`
        """
        pass
