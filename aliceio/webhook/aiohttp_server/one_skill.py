import json
from typing import Any, Optional

from aiohttp import web

from aliceio import Dispatcher, Skill, loggers
from aliceio.types import Update
from aliceio.webhook.aiohttp_server.base import (
    BaseAiohttpRequestHandler,
    _JsonDumps,
    _JsonLoads,
)


class OneSkillAiohttpRequestHandler(BaseAiohttpRequestHandler):
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
        update = await self._validate_update(skill, request)

        # Проверка айди навыка в поступившем событии
        if update.session.skill_id != skill.skill_id:
            loggers.webhook.warning(
                "Update came from a skill id=%r, but was expected skill id=%r",
                update.session.skill_id,
                skill.skill_id,
            )
            return web.Response(body="Not Acceptable", status=406)

        return await super()._handle_request(skill, request, update)
