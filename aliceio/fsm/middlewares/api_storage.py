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

    Регистрируется только тогда, когда установлен флаг при создании диспетчера.

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

        await self.set_state_from_alice(event, fsm_context)
        data[RAW_STATE_KEY] = await fsm_context.get_state()

        response: Optional[AliceResponse] = await handler(event, data)

        if response:
            await self.set_state_to_alice(
                response,
                fsm_context,
                event.session.is_anonymous,
            )

        # Очистка ключа, так как невозможно изменить состояние не через ответ на запрос
        await fsm_context.clear()

        return response

    async def set_state_from_alice(
        self,
        event: Update,
        fsm_context: FSMContext,
    ) -> None:
        state = self.resolve_state_data(event.state)
        await fsm_context.set_state(state.state)
        await fsm_context.set_data(state.data)

    def resolve_state_data(self, state: Optional[ApiState]) -> ApiStorageRecord:
        if state is None:
            return self.create_record_from_data({})
        if self.strategy == FSMStrategy.USER:
            # Если анонимный пользователь (Алиса не отправляет state.user),
            # то сохраняем состояние по устройству
            if state.user is None:
                return self.create_record_from_data(state.application)
            return self.create_record_from_data(state.user)
        if self.strategy == FSMStrategy.SESSION:
            return self.create_record_from_data(state.session)
        if self.strategy == FSMStrategy.APPLICATION:
            return self.create_record_from_data(state.application)
        return self.create_record_from_data(state.session)

    def create_record_from_data(self, data: Dict[str, Any]) -> ApiStorageRecord:
        return ApiStorageRecord(data=data.get("data", {}), state=data.get("state"))

    async def set_state_to_alice(
        self,
        response: AliceResponse,
        fsm_context: FSMContext,
        is_anonymous: bool = False,
    ) -> None:
        new_state = {
            "state": await fsm_context.get_state(),
            "data": await fsm_context.get_data(),
        }
        self.set_new_state(response, new_state, is_anonymous)

    def set_new_state(
        self,
        response: AliceResponse,
        new_state: Dict[str, Any],
        is_anonymous: bool = False,
    ) -> None:
        if self.strategy == FSMStrategy.USER:
            if is_anonymous:
                # Если анонимный пользователь и стратегия по юзеру,
                # то сохраняем состояние по устройству
                response.application_state = new_state
            else:
                response.user_state_update = new_state
        elif self.strategy == FSMStrategy.SESSION:
            response.session_state = new_state
        elif self.strategy == FSMStrategy.APPLICATION:
            response.application_state = new_state
        else:
            response.session_state = new_state
