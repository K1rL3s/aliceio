from __future__ import annotations

import io
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Union

import aiofiles

DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 kb


class InputFile(ABC):
    """
    Этот объект представляет содержимое загружаемого файла.

    Должно быть опубликовано с использованием multipart/form-data обычным способом,
    которым файлы загружаются через браузер.
    """

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Базовый класс для файлов. Не следует использовать напрямую.
        См. :class:`BufferedInputFile`, :class:`FSInputFile` и :class:`URLInputFile`

        :param chunk_size: Размер блоков чтения.
        """
        self.chunk_size = chunk_size

    @abstractmethod
    async def read(self) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class BufferedInputFile(InputFile):
    def __init__(
        self,
        file: bytes,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Представляет объект для загрузки файлов из файловой системы.

        :param file: Байты.
        :param chunk_size: Размер загружаемых фрагментов.
        """
        super().__init__(chunk_size=chunk_size)

        self.data = file

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> BufferedInputFile:
        """
        Создать буфер из файла.

        :param path: Путь до файла.
        :param chunk_size: Размер загружаемых фрагментов.
        :return: Экземпляр :obj:`BufferedInputFile`
        """
        with open(path, "rb") as f:
            data = f.read()
        return cls(data, chunk_size=chunk_size)

    async def read(self) -> AsyncGenerator[bytes, None]:
        buffer = io.BytesIO(self.data)
        while chunk := buffer.read(self.chunk_size):
            yield chunk


class FSInputFile(InputFile):
    def __init__(
        self,
        path: Union[str, Path],
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """
        Представляет объект для загрузки файлов из файловой системы.

        :param path: Путь до файла.
        :param chunk_size: Размер загружаемых фрагментов.
        """
        super().__init__(chunk_size=chunk_size)

        self.path = path

    async def read(self) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(self.path, "rb") as f:
            while chunk := await f.read(self.chunk_size):
                yield chunk
