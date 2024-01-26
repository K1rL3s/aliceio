from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional, TypeVar, Union, overload

from ..methods import (
    DeleteImage,
    DeleteSound,
    GetImages,
    GetSounds,
    Status,
    UploadImage,
    UploadSound,
)
from ..methods.base import AliceMethod
from ..types import (
    InputFile,
    PreUploadedImage,
    PreUploadedSound,
    Result,
    SpaceStatus,
    UploadedImagesList,
    UploadedSoundsList,
)
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
            Зайдите на страницу навыка, откройте вкладку "Общие сведения"
            и пролистайте вниз. Запросы без этого айди будут игнорироваться.\n
        :param oauth_token: Токен для загрузки аудио и изображений.
            Без [этого](https://yandex.ru/dev/direct/doc/start/token.html) токена нельзя взаимодействовать с API Алисы.\n
        :param session: HTTP Client session (Например, AiohttpSession).
            Если не указано, будет создано автоматически.
        """
        if session is None:
            session = AiohttpSession()

        self.session = session
        self.__skill_id = skill_id
        self.__oauth_token = oauth_token

    @property
    def token(self) -> Optional[str]:
        return self.__oauth_token

    @property
    def oauth_token(self) -> Optional[str]:
        return self.__oauth_token

    @property
    def skill_id(self) -> str:
        return self.__skill_id

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

        :param method: Запрос, наследник :code:`AliceMethod`.
        :return:
        """
        return await self.session(self, method.as_(self), timeout=request_timeout)

    async def status(self, request_timeout: Optional[int] = None) -> SpaceStatus:
        status = Status()
        return await self(status, request_timeout=request_timeout)

    async def get_images(
        self,
        request_timeout: Optional[int] = None,
    ) -> UploadedImagesList:
        get_images = GetImages()
        return await self(get_images, request_timeout=request_timeout)

    @overload
    async def upload_image(
        self,
        url: str,
        /,
        request_timeout: Optional[int] = None,
    ) -> PreUploadedImage:
        pass

    @overload
    async def upload_image(
        self,
        file: InputFile,
        /,
        request_timeout: Optional[int] = None,
    ) -> PreUploadedImage:
        pass

    async def upload_image(
        self,
        file: Union[InputFile, str],
        request_timeout: Optional[int] = None,
    ) -> PreUploadedImage:
        if isinstance(file, str):
            upload_image = UploadImage(url=file)
        else:
            upload_image = UploadImage(file=file)
        return await self(upload_image, request_timeout=request_timeout)

    async def delete_image(
        self,
        file_id: str,
        request_timeout: Optional[int] = None,
    ) -> Result:
        delete_image = DeleteImage(file_id=file_id)
        return await self(delete_image, request_timeout=request_timeout)

    async def get_sounds(
        self,
        request_timeout: Optional[int] = None,
    ) -> UploadedSoundsList:
        get_sounds = GetSounds()
        return await self(get_sounds, request_timeout=request_timeout)

    async def upload_sound(
        self,
        file: InputFile,
        request_timeout: Optional[int] = None,
    ) -> PreUploadedSound:
        upload_sound = UploadSound(file=file)
        return await self(upload_sound, request_timeout=request_timeout)

    async def delete_sound(
        self,
        file_id: str,
        request_timeout: Optional[int] = None,
    ) -> Result:
        delete_sound = DeleteSound(file_id=file_id)
        return await self(delete_sound, request_timeout=request_timeout)
