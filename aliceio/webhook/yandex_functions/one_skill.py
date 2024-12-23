from typing import Any, Optional

from aliceio import Dispatcher, Skill, loggers
from aliceio.types import Update

from .base import BaseYandexFunctionsRequestHandler, _Event, _Response
from .context import RuntimeContext


class OneSkillYandexFunctionsRequestHandler(BaseYandexFunctionsRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        skill: Skill,
        **data: Any,
    ) -> None:
        """
        Обработчик запросов в облачных функциях Яндекса для одного экземпляра навыка.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        :param skill: Экземпляр :class:`aliceio.client.skill.Skill`
        """
        super().__init__(dispatcher=dispatcher, **data)
        self.skill = skill

    async def resolve_skill(self, event: _Event, context: RuntimeContext) -> Skill:
        return self.skill

    async def _handle_request(
        self,
        skill: Skill,
        event: _Event,
        context: RuntimeContext,
        update: Optional[Update] = None,
    ) -> _Response:
        update = await self._validate_update(skill, event, context)

        # Проверка айди навыка в поступившем событии
        if update.session.skill_id != skill.skill_id:
            loggers.yandex_funcs.warning(
                "Update came from a skill id=%r, but was expected skill id=%r",
                update.session.skill_id,
                skill.skill_id,
            )
            return None

        return await super()._handle_request(skill, event, context, update=update)
