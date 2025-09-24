import logging
from typing import TYPE_CHECKING, Any, Optional

from aliceio import loggers
from aliceio.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from aliceio.methods import AliceMethod
from aliceio.methods.base import AliceType, ApiResponse

if TYPE_CHECKING:
    from aliceio.client.skill import Skill

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    """
    Мидлварь для логгирования исходящих запросов.

    :param ignore_methods: Ингорируемые методы при логгировании
    """

    def __init__(
        self,
        ignore_methods: Optional[list[type[AliceMethod[Any]]]] = None,
    ) -> None:
        self.ignore_methods = ignore_methods or []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[AliceType],
        skill: "Skill",
        method: AliceMethod[AliceType],
    ) -> ApiResponse[AliceType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by skill id=%r",
                type(method).__name__,
                skill.id,
            )
        return await make_request(skill, method)
