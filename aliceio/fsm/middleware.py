from typing import Any, Awaitable, Callable, Dict, Optional, cast

from aliceio import Skill
from aliceio.dispatcher.middlewares.base import BaseMiddleware
from aliceio.fsm.context import FSMContext
from aliceio.fsm.storage.base import DEFAULT_DESTINY, BaseStorage, StorageKey
from aliceio.fsm.strategy import FSMStrategy, apply_strategy
from aliceio.types import Session, User
from aliceio.types.base import AliceObject


class FSMContextMiddleware(BaseMiddleware):
    def __init__(
        self,
        storage: BaseStorage,
        strategy: FSMStrategy = FSMStrategy.USER,
    ) -> None:
        self.storage = storage
        self.strategy = strategy

    async def __call__(
        self,
        handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]],
        event: AliceObject,
        data: Dict[str, Any],
    ) -> Any:
        skill: Skill = cast(Skill, data["skill"])
        context = self.resolve_event_context(skill, data)
        data["fsm_storage"] = self.storage
        if context:
            data.update({"state": context, "raw_state": await context.get_state()})
        return await handler(event, data)

    def resolve_event_context(
        self,
        skill: Skill,
        data: Dict[str, Any],
        destiny: str = DEFAULT_DESTINY,
    ) -> Optional[FSMContext]:
        session: Session = data["event_session"]
        user: Optional[User] = data.get("event_from_user")
        user_id = user.user_id if user else session.application.application_id
        return self.resolve_context(
            skill=skill,
            user_id=user_id,
            session_id=session.session_id,
            destiny=destiny,
        )

    def resolve_context(
        self,
        skill: Skill,
        user_id: str,
        session_id: str,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext:
        user_id, session_id = apply_strategy(
            strategy=self.strategy,
            user_id=user_id,
            session_id=session_id,
        )
        return self.get_context(
            skill=skill,
            user_id=user_id,
            session_id=session_id,
            destiny=destiny,
        )

    def get_context(
        self,
        skill: Skill,
        user_id: str,
        session_id: str,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext:
        return FSMContext(
            storage=self.storage,
            key=StorageKey(
                skill_id=skill.id,
                user_id=user_id,
                session_id=session_id,
                destiny=destiny,
            ),
        )

    async def close(self) -> None:
        await self.storage.close()
