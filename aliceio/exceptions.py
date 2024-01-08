from typing import Optional

from aliceio.methods.base import AliceMethod, AliceType


class AliceioError(Exception):
    """Базовое исключение для всех ошибок aliceio."""


class DetailedAliceioError(AliceioError):
    """Базовое исключение для всех ошибок aliceio с подробным сообщением."""

    url: Optional[str] = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class AliceAPIError(DetailedAliceioError):
    """Базовое исключение для всех ошибок API Алисы."""

    label: str = "Alice's server says"

    def __init__(
        self,
        method: AliceMethod[AliceType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"
