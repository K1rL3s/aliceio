# Класс BaseMiddleware
`BaseMiddleware(ABC)` - Базовый дженерик мидлварь

### Функции
- `__call__(self, handler: Callable[[AliceObject, Dict[str, Any]], Awaitable[Any]], event: AliceObject, data: Dict[str, Any],) -> Any`\
Вызов мидлваря.
- **Параметры**\
    `handler` - Обёрнутый обработчик в цепочке мидлварей\
    `event` - Входящее событие(Подклас :class:`aliceio.types.base.AliceObject`)\
    `data` - Данные контекста. Будет сопоставлен с аргументами обработчика.

[Пример](https://github.com/K1rL3s/aliceio/blob/examples/examples/context_addition.py)
