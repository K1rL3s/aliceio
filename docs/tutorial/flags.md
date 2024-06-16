# Флаги

Флаги - это некие «маркеры» для хэндлеров. Флаги могут быть добавлены в хендлер с помощью декораторов или фильтров.\
Например с помощью флагов можно пометить хэндлеры, не влезая в их внутреннюю структуру, чтобы затем что-то сделать в мидлварях, например, троттлинг.


### С помощью декораторов
```
@flags.chat_action
async def my_handler(message: Message)
```
или для ограничения скорости или чего-нибудь ещё
```
@flags.rate_limit(rate=2, key="something")
async def my_handler(message: Message)
```
### С помощью регистрации методов
```
@router.message(...,flags={'chat_action':'typing','rate_limit':{'rate':5}})
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
        processing = get_flag(data, "processing")
        if not processing:
            return await handler(event, data)

        bot_msg = await event.answer(text=PROCESSING)
        try:
            return await handler(event, data)
        finally:
            await bot_msg.delete()
```

* [Пример из гайда МастераГруши на aiogram](https://mastergroosha.github.io/aiogram-3-guide/filters-and-middlewares/#flags){:target="_blank"}
* [Пример флага в мидлваре из проекта на aiogram](https://github.com/K1rL3s/PROD-Travel-Bot/blob/main/src/bot/middlewares/inner/processing.py#L20){:target="_blank"}
