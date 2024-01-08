from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, AsyncIterator, Optional, TypeVar

import aiofiles

from ..methods.base import AliceMethod
from .session.aiohttp import AiohttpSession
from .session.base import BaseSession

T = TypeVar("T")


class Skill:
    def __init__(
        self,
        skill_id: str,
        oauth_token: Optional[str] = None,
        session: Optional[BaseSession] = None,
    ) -> None:
        """
        Класс Навыка.

        :param skill_id: Идентификатор навыка можно посмотреть в консоли разработчика.
                         Зайдите на страницу навыка, откройте вкладку Общие сведения
                         и пролистайте вниз.
        :param oauth_token: Токен для загрузки аудио и изображений,
                            https://yandex.ru/dev/direct/doc/start/token.html
        :param session: HTTP Client session (Например, AiohttpSession).
                        Если не указано, будет создано автоматически.
        """
        if session is None:
            session = AiohttpSession()

        self.session = session
        self.__skill_id = skill_id
        self.__oauth_token = oauth_token

    @property
    def token(self) -> str:
        return self.__oauth_token

    @property
    def oauth_token(self) -> str:
        return self.__oauth_token

    @property
    def id(self) -> str:
        return self.__skill_id

    @asynccontextmanager
    async def context(self, auto_close: bool = True) -> AsyncIterator[Skill]:
        """
        Использование в контекстном менеджере.

        :param auto_close: Закрыть ли HTTP-сессию при выходе.
        :return: Skill
        """
        try:
            yield self
        finally:
            if auto_close:
                await self.session.close()

    @classmethod
    async def __aiofiles_reader(
        cls,
        file: str,
        chunk_size: int = 65536,
    ) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(file, "rb") as f:
            while chunk := await f.read(chunk_size):
                yield chunk

    def __eq__(self, other: Any) -> bool:
        """
        Сравнить текущий навык с другим экземпляром навыка.

        :param other:
        :return:
        """
        if not isinstance(other, Skill):
            return False
        return self.id == other.id

    async def __call__(
        self,
        method: AliceMethod[T],
        request_timeout: Optional[int] = None,
    ) -> T:
        """
        Вызов API Алисы.

        :param method: Запрос, наследник :code:`AliceMethod`
        :return:
        """
        return await self.session(self, method, timeout=request_timeout)
