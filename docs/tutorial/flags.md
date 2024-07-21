# Флаги

Флаги - это некие «маркеры» для обработчиков. Флаги могут быть добавлены в хендлер с помощью декораторов или фильтров.\
Например, с помощью флагов можно пометить хэндлеры, не влезая в их внутреннюю структуру, чтобы затем что-то сделать в мидлварях.


### С помощью декораторов
```
@flags.some_flag_name
async def my_handler(message: Message):
    ...
```
```
@flags.other_name(foo="bar", key=42)
async def my_handler(message: Message):
    ...
```

### С помощью регистрации методов
```
@router.message(..., flags={"foo": "bar", "key": 42)
```

### С помощью фильтров
```
class Command(Filter):
    ...

    def update_handler_flags(self, flags: Dict[str, Any]) -> None:
        commands = flags.setdefault("commands", [])
        commands.append(self)
```

### Синтаксис в мидлваре
```
class ProcessingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        some_flag = get_flag(data, "some_flag_name")
        if some_flag:
            ...

        return await handler(event, data)
```

* [aiogram](https://docs.aiogram.dev/en/latest/dispatcher/flags.html)
* [Пример из гайда МастераГруши на aiogram](https://mastergroosha.github.io/aiogram-3-guide/filters-and-middlewares/#flags){:target="_blank"}
