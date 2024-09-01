# Внедрение зависимостей

DI - это метод программирования, который делает класс независимым от его зависимостей.
Это достигается путем отделения использования объекта от его создания.
Это поможет вам следовать принципу инверсии зависимостей [SOLID](https://en.wikipedia.org/wiki/SOLID){:target="_blank"} и принципу единой ответственности.

## Как это работает в aliceio

Для каждого события в `aliceio.dispatcher.dispatcher.Dispatcher` проходит обработка контекстных данных. Фильтры и мидлвари также могут вносить изменения в контекст.

Для доступа к контекстным данным необходимо указать соответствующий ключевой параметр в хэндлере или фильтре.
Например, чтобы получить `aliceio.fsm.context.FSMContext`, достаточно сделать так:

```python
@router.message(...)
async def some_message(message: Message, skill: Skill, state: FSMContext) -> Any:
    ... # do something
```

## Внедрение собственных зависимостей

Aliceio предоставляет несколько способов дополнения и изменения контекстных данных.

### Инициализация

Первый и самый простой способ - просто указать именованные аргументы при иницализации `aliceio.dispatcher.dispatcher.Dispatcher` или `aliceio.webhook.aiohttp_server.OneSkillAiohttpRequestHandler`.

```python
def main() -> None:
    dp = Dispatcher(..., foo=42)
    ...
```
```python
def main() -> None:
    dp = Dispatcher(..., foo=42)
    handler = OneSkillAiohttpRequestHandler(dispatcher=dp, skill=skill, bar="Bazz")
    ...
```

Также можно изменять workflow_data в `aliceio.dispatcher.dispatcher.Dispatcher` как словарь:

```python
dp = Dispatcher(...)
dp["eggs"] = Spam()
```

### Мидлвари

Мидлвари также могут изменять контекст:

```python
class RandomFloatMiddleware(BaseMiddleware[Message]):
    def __init__(self, start: float = 0.01, end: float = 100.0) -> None:
        self.start = start
        self.end = end

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Добаляем значение в контекст
        data["float_num"] = round(random.uniform(self.start, self.end), 3)
        return await handler(event, data)
```

### Фильтры

Фильтры могут дополнять контекстные данные:

```python
class RandomNumberFilter(BaseFilter):
    async def __call__(
        self,
        message: Message,
        event_from_user: User
        # Фильтры также могут принимать данные из контекста как обработчики
    ) -> Union[bool, Dict[str, Any]]:
        if message.command == "число":
            # Возврат словаря обновит контекст
            return {"int_num": random.randint(1_000, 10_000)}
        return False
```

Или через `MagicFilter` с помощью метода `.as_(...)`:

```python
@router.message(F.text.as_("real_text"), ~F.session.new)
async def start_handler(message: Message, real_text: str) -> str:
    assert real_text == message.text
    return real_text
```

## Примеры

* [context_addition.py](https://github.com/K1rL3s/aliceio/blob/master/examples/context_addition.py){:target="_blank"}
* [aiogram](https://docs.aiogram.dev/en/dev-3.x/dispatcher/dependency_injection.html){:target="_blank"}
