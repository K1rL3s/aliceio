from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, cast

from pydantic import BaseModel

from aliceio import Dispatcher, Skill
from aliceio.types import Update
from aliceio.types.base import AliceObject
from aliceio.utils.funcs import prepare_value

_Event = Dict[str, Any]
_Context = Dict[str, Any]
_Response = Optional[Dict[str, Any]]


class BaseYandexFunctionsRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        **data: Any,
    ) -> None:
        """
        Базовый обработчик, который помогает обрабатывать входящий запрос от aiohttp
        и передавать его диспетчеру.

        :param dispatcher: Экземпляр :class:`aliceio.dispatcher.dispatcher.Dispatcher`
        """
        self.dispatcher = dispatcher
        self.data = data

    @abstractmethod
    async def _handle_request(
        self,
        skill: Skill,
        event: _Event,
        context: _Context,
        update: Optional[Update] = None,
    ) -> _Response:
        if update is None:
            update = await self._validate_update(skill, event, context)

        result = await self.dispatcher.feed_webhook_update(
            skill,
            update,
            **self.data,
        )
        return self._build_response(result)

    @abstractmethod
    async def resolve_skill(self, event: _Event, context: _Context) -> Skill:
        pass

    async def _validate_update(
        self,
        skill: Skill,
        event: _Event,
        context: _Context,
    ) -> Update:
        json_data = self._convert_show_pull_to_normal_request(event)
        return Update.model_validate(json_data, context={"skill": skill})

    async def handle(self, event: _Event, context: _Context) -> _Response:
        skill = await self.resolve_skill(event, context)
        return await self._handle_request(skill=skill, event=event, context=context)

    __call__ = handle

    # TODO: Проверить, помогает ли про запуске шоу Алисы
    @staticmethod
    def _convert_show_pull_to_normal_request(event: _Event) -> _Event:
        """
        При получении события запуска утреннего шоу вся информация
        (мета, сессия, версия и реквест) вероятно находится по ключу body.
        Эта функция выносит всю информацию за это поле.

        https://yandex.ru/dev/dialogs/alice/doc/ru/request-show-pull

        :param event:
        :return:
        """
        return cast(Dict[str, Any], event.get("body", event))

    def _build_response(self, result: Optional[AliceObject]) -> _Response:
        return cast(
            _Response,
            prepare_value(
                value=result.model_dump() if isinstance(result, BaseModel) else result,
                files={},
            ),
        )
