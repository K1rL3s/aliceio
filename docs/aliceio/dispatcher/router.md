::: aliceio.dispatcher.router.Router
    handler: python
    options:
      merge_init_into_class: false
      members:
        - __init__
        - include_router
        - include_routers


## Наблюдатели

!!! warning "Важно"
    Все хэндлеры всегда должны быть асинхронными. Имя функции-обработчика не имеет значения.
    Имя аргумента события также не важно, но рекомендуется не перекрывать имя контекстными данными, поскольку функция не может принимать два аргумента с одинаковым именем.

Вот список всех доступных наблюдателей и примеры регистрации хэндлеров.

В этих примерах используется только регистрация через декоратор, но вы всегда можете использовать метод `<router>.<event_type>.register(...)`

### Сообщение (SimpleUtterance)
```python
@router.message()
async def message_handler(message: Message) -> Any: pass
```

### Нажатие на кнопку
```python
@router.button_pressed()
async def button_pressed_handler(button: ButtonPressed) -> Any: pass
```

### Аудиоплеер
```python
@router.audio_player()
async def audio_player_handler(audio_player: AudioPlayer) -> Any: pass
```


### Покупка
```python
@router.purchase()
async def purchase_handler(purchase: Purchase) -> Any: pass
```

### Показ шоу
```python
@router.show_pull()
async def show_pull_handler(pull: ShowPull) -> Any: pass
```

## Вложенные роутеры

Событие будет распространять по роутерам и хэндлерам согласно порядку их добавления.

!!! warning "Важно"
    Роутеры могут быть включены в другие роутеры с некоторыми ограничениями:

    1. Роутер не может подключить сам себя
    2. Роутеры не могут составлять цикл (р1 содержит р2, р2 содержит р3, р3 содерит р1)

## Update
```python
@dispatcher.update()
async def update_handler(update: Update) -> Any: pass
```

!!! warning "Предупреждение"
    Только диспетчер может обрабатывать события с типом `Update`.

!!! note "Примечание"
    В диспетчере уже есть обработчик этого типа событий, поэтому вы можете использовать его для обработки всех обновлений, которые не обработались другими хэндлерами.


## Источники

* [aiogram](https://docs.aiogram.dev/en/dev-3.x/dispatcher/router.html){:target="_blank"}
