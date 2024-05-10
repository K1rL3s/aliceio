from collections import deque
from typing import TYPE_CHECKING, Any, AsyncGenerator, Deque, Dict, Optional, Type

from aliceio import Skill
from aliceio.client.session.base import BaseSession
from aliceio.methods import AliceMethod
from aliceio.methods.base import AliceType, ApiResponse


class MockedSession(BaseSession):
    def __init__(self) -> None:
        super().__init__()
        self.responses: Deque[ApiResponse[AliceType]] = deque()
        self.requests: Deque[AliceMethod[AliceType]] = deque()
        self.closed = True

    def add_result(self, response: ApiResponse[AliceType]) -> ApiResponse[AliceType]:
        self.responses.append(response)
        return response

    def get_request(self) -> AliceMethod[AliceType]:
        return self.requests.pop()

    async def close(self) -> None:
        self.closed = True

    async def make_request(
        self,
        skill: Skill,
        method: AliceMethod[AliceType],
        timeout: Optional[int] = None,
    ) -> AliceType:
        self.closed = False
        self.requests.append(method)
        response: ApiResponse[AliceType] = self.responses.pop()
        result = response.result
        self.check_response(
            skill=skill,
            method=method,
            status_code=response.status_code,
            content=result.model_dump_json(),
        )
        return response.result  # type: ignore

    async def stream_content(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class MockedSkill(Skill):
    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs) -> None:
        super().__init__(
            kwargs.pop("token", "42:SKILL_ID"),
            session=MockedSession(),
            **kwargs,
        )

    def add_result_for(
        self,
        method: Type[AliceMethod[AliceType]],
        result: Optional[AliceType] = None,
        status_code: int = 200,
    ) -> ApiResponse[AliceType]:
        response = ApiResponse[method.__returning__](  # type: ignore
            result=result,
            status_code=status_code,
        )
        self.session.add_result(response)
        return response

    def get_request(self) -> AliceMethod[AliceType]:
        return self.session.get_request()
