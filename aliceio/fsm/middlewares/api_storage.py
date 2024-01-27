from typing import Any, Awaitable, Callable, Dict, Optional

from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.fsm.context import FSMContext
from aliceio.fsm.middlewares.fsm_context import FSM_CONTEXT_KEY, RAW_STATE_KEY
from aliceio.fsm.storage.api import ApiStorageRecord
from aliceio.fsm.strategy import FSMStrategy
from aliceio.types import AliceResponse, ApiState, Update


class FSMApiStorageMiddleware(BaseMiddleware[Update]):
    """
    Заполняет экземпляр FSMContext данными из состояний API Алисы.

    Устанавливается только тогда, когда установлен флаг при создании диспетчера.

    https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html
    """

    def __init__(self, strategy: FSMStrategy = FSMStrategy.USER):
        self.strategy = strategy

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        fsm_context: FSMContext = data[FSM_CONTEXT_KEY]

        await self.pre_set_state(event, fsm_context)
        data.update({RAW_STATE_KEY: await fsm_context.get_state()})

        response: Optional[AliceResponse] = await handler(event, data)

        if response:
            await self.post_update_state(response, fsm_context)

        # Очистка ключа, так как невозможно изменить состояние не через ответ на запрос
        await fsm_context.clear()

        return response

    async def pre_set_state(self, event: Update, fsm_context: FSMContext) -> None:
        state = self.resolve_state_data(event.state)
        await fsm_context.set_state(state.state)
        await fsm_context.set_data(state.data)

    def resolve_state_data(self, state: ApiState) -> ApiStorageRecord:
        if self.strategy == FSMStrategy.USER:
            return self._data_to_record(state.user)
        if self.strategy == FSMStrategy.SESSION:
            return self._data_to_record(state.session)
        if self.strategy == FSMStrategy.APPLICATION:
            return self._data_to_record(state.application)
        return self._data_to_record(state.session)

    @staticmethod
    def _data_to_record(data: Dict[str, Any]) -> ApiStorageRecord:
        return ApiStorageRecord(data=data.get("data", {}), state=data.get("state"))

    async def post_update_state(
        self,
        response: AliceResponse,
        fsm_context: FSMContext,
    ) -> None:
        new_state = {
            "state": await fsm_context.get_state(),
            "data": await fsm_context.get_data(),
        }
        self.set_new_state(response, new_state)

    def set_new_state(
        self,
        response: AliceResponse,
        new_state: Dict[str, Any],
    ) -> None:
        if self.strategy == FSMStrategy.USER:
            response.user_state_update = new_state
        elif self.strategy == FSMStrategy.SESSION:
            response.session_state = new_state
        elif self.strategy == FSMStrategy.APPLICATION:
            response.application_state = new_state
        else:
            response.session_state = new_state
