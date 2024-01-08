from __future__ import annotations

import io
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, Optional, Union

import aiofiles

if TYPE_CHECKING:
    from aliceio.client.skill import Skill

DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 kb


class InputFile(ABC):
    """
    Этот объект представляет содержимое загружаемого файла.

    Должно быть опубликовано с использованием multipart/form-data обычным способом,
    которым файлы загружаются через браузер.
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Базовый класс для файлов. Не следует использовать напрямую.
        См. :class:`BufferedInputFile`, :class:`FSInputFile` :class:`URLInputFile`

        :param filename: Имя данного файла.
        :param chunk_size: Размер блоков чтения.
        """
        self.filename = filename
        self.chunk_size = chunk_size

    @abstractmethod
    async def read(
        self,
        skill: "Skill",
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class BufferedInputFile(InputFile):
    def __init__(
        self,
        file: bytes,
        filename: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Представляет объект для загрузки файлов из файловой системы.

        :param file: Байты.
        :param filename: Имя файла, которое будет передано в Алису.
        :param chunk_size: Размер загружаемых фрагментов.
        """
        super().__init__(filename=filename, chunk_size=chunk_size)

        self.data = file

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> BufferedInputFile:
        """
        Создать буфер из файла.

        :param path: Путь до файла.
        :param filename: Имя файла, которое будет передано в Алису.
                         По умолчанию будет взято из пути.
        :param chunk_size: Размер загружаемых фрагментов.
        :return: Экземпляр :obj:`BufferedInputFile`
        """
        if filename is None:
            filename = os.path.basename(path)
        with open(path, "rb") as f:
            data = f.read()
        return cls(data, filename=filename, chunk_size=chunk_size)

    async def read(self, skill: "Skill") -> AsyncGenerator[bytes, None]:
        buffer = io.BytesIO(self.data)
        while chunk := buffer.read(self.chunk_size):
            yield chunk


class FSInputFile(InputFile):
    def __init__(
        self,
        path: Union[str, Path],
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Представляет объект для загрузки файлов из файловой системы.

        :param path: Путь до файла.
        :param filename: Имя файла, которое будет передано в Алису.
                         По умолчанию будет взято из пути.
        :param chunk_size: Размер загружаемых фрагментов.
        """
        if filename is None:
            filename = os.path.basename(path)
        super().__init__(filename=filename, chunk_size=chunk_size)

        self.path = path

    async def read(self, skill: "Skill") -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(self.path, "rb") as f:
            while chunk := await f.read(self.chunk_size):
                yield chunk


class URLInputFile(InputFile):
    def __init__(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        timeout: int = 30,
    ) -> None:
        """
        Представляет объект для файлов из Интернета.

        :param url: URL в Интернете.
        :param headers: HTTP-заголовки.
        :param filename: Имя файла, которое будет передано в Алису.
        :param chunk_size: Размер загружаемых фрагментов.
        :param timeout: Таймаут для скачивания.
        """
        super().__init__(filename=filename, chunk_size=chunk_size)
        if headers is None:
            headers = {}

        self.url = url
        self.headers = headers
        self.timeout = timeout

    async def read(self, skill: "Skill") -> AsyncGenerator[bytes, None]:
        stream = skill.session.stream_content(
            url=self.url,
            headers=self.headers,
            timeout=self.timeout,
            chunk_size=self.chunk_size,
            raise_for_status=True,
        )

        async for chunk in stream:
            yield chunk
