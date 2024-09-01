from typing import Any, Optional

from aliceio import Dispatcher, Skill, loggers
from aliceio.types import Update
from aliceio.webhook.yandex_functions.base import (
    BaseYandexFunctionsRequestHandler,
    _Context,
    _Event,
    _Response,
)


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

    async def close(self) -> None:
        """Закрыть сессию навыка."""
        await self.skill.session.close()

    async def resolve_skill(self, event: _Event, context: _Context) -> Skill:
        return self.skill

    async def _handle_request(
        self,
        skill: Skill,
        event: _Event,
        context: _Context,
        update: Optional[Update] = None,
    ) -> _Response:
        update = await self._update_validate(skill, event, context)

        # Проверка айди навыка в поступившем событии
        if update.session.skill_id != skill.skill_id:
            loggers.yandex_funcs.warning(
                "Update came from a skill id=%r, but was expected skill id=%r",
                update.session.skill_id,
                skill.skill_id,
            )
            return None

        return await super()._handle_request(skill, event, context, update=update)
