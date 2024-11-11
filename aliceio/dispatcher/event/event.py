from typing import Any, Callable

from .handler import CallbackType, HandlerObject


class EventObserver:
    """
    Простой отслеживатель событий.

    Используется для управления событиями, не связанными с Алисой
    (например, запуск/выключение).

    Обработчики можно зарегистрировать через метод или декоратор:
    ``` py
    <observer>.register(my_handler)
    ```
    ``` py
    @<observer>()
    async def my_handler(*args, **kwargs): ...
    ```
    """

    def __init__(self) -> None:
        self.handlers: list[HandlerObject] = []

    def register(self, callback: CallbackType) -> None:
        """Регистрация callback'а."""
        self.handlers.append(HandlerObject(callback=callback))

    async def trigger(self, *args: Any, **kwargs: Any) -> None:
        """Распространение события на обработчики."""
        for handler in self.handlers:
            await handler.call(*args, **kwargs)

    def __call__(self) -> Callable[[CallbackType], CallbackType]:
        """Декоратор для регистрации обработчиков."""

        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(callback)
            return callback

        return wrapper
