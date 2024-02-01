# Особые события

## Таймаут

Таймаут-событие возникает, когда время обработки запроса на стороне навыка длиться дольше 4 секунд (по умолчанию).

Если хэндлер находится в режиме ожидания выполнения чего-то асинхронного, то диспетчер остановит обработку события и создаст "экстренное" событие таймаута.

Его можно обработать также, как и любое другое входящее событие:

```python
@router.timeout()
async def timeout_handler(event: TimeoutUpdate) -> str:
    return "У меня что-то пошло не так, я какой-то долгодум..."
```

!!! warning "Важно"
    От таких хэндлеров требуется молниеносный ответ. В них не должно быть ничего, что может долго работать.

    Если навык ничего не ответит, то Алиса завершит сессию.

### Таймаут-событие

### ::: aliceio.types.timeout_event.TimeoutUpdate
    handler: python
    options:
      members:
        - event
        - event_type

## Запуск и завершение

В диспетчере можно зарегистрировать вспомогательные функции на включение и выключение.

В них можно, например, инициализировать подключение к бд или проверить место для файлов навыка:

```python
@dispatcher.startup()
async def on_startup(skill: Skill) -> None:
    space: SpaceStatus = await skill.status()
    if space.images.quota.available < 1024 or space.sounds.quota.available < 1024:
        exit("ALARM!!! NOT ENOUGH SPACE")
```
```python
async def on_shutdown() -> None:
    await close_all_sessions()

dispatcher.shutdown.register(on_shutdown)
```

## Примеры

* [on_dispatcher_event.py](https://github.com/K1rL3s/aliceio/blob/master/examples/on_dispatcher_event.py)
