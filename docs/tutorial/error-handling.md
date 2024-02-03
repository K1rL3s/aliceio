# Обработка исключений

Рекомендуемый способ обработки ошибок - это блок `try except` внутри хэндлера,
но для общих случаев вы можете добавить обработчик ошибок на уровень роутера или диспетчера.

```python
@router.error(ExceptionTypeFilter(MyCustomException), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    # do something with error
    await message.answer("Oops, something went wrong!")


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    # do something with error
    ...
```

## Событие исключения

::: aliceio.types.error_event.ErrorEvent
    handler: python
    options:
      show_source: false
      members:
        - event
        - exception
        - update

## Исключения библиотеки

### ::: aliceio.exceptions.AliceioError
    handler: python
    options:
      show_source: false

### ::: aliceio.exceptions.DetailedAliceioError
    handler: python
    options:
      show_source: false
    members:
      - url
      - message

### ::: aliceio.exceptions.AliceAPIError
    handler: python
    options:
      show_source: false

### ::: aliceio.exceptions.AliceNetworkError
    handler: python
    options:
      show_source: false

### ::: aliceio.exceptions.AliceNoCredentialsError
    handler: python
    options:
      show_source: false

### ::: aliceio.exceptions.AliceWrongFieldError
    handler: python
    options:
      show_source: false

### ::: aliceio.exceptions.ClientDecodeError
    handler: python
    options:
      show_source: false
      members:
        - message
        - original
        - data

## Примеры

* [error_handling.py](https://github.com/K1rL3s/aliceio/blob/master/examples/error_handling.py){:target="_blank"}
