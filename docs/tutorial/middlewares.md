# Мидлвари

aliceio предоставляет мощный механизм настройки обработчиков событий через мидлвари.

Мидлвари здесь похожи на мидлвари в веб-фреймворках, таких как
[aiohttp](https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-middlewares){:target="_blank"},
[fastapi](https://fastapi.tiangolo.com/tutorial/middleware/){:target="_blank"},
[Django](https://docs.djangoproject.com/en/5.0/topics/http/middleware/){:target="_blank"} и т.д.
с небольшой разницей - здесь реализованы два уровня промежуточного программного обеспечения (до и после фильтров).

!!! info "Примечание"
    Мидлварь - это код, который активируется при каждом событии, полученном от API Алисы.

## Теория

Как говорится во многих книгах и другой литературе в Интернете:
> Мидлвари — это повторно используемое программное обеспечение, которое использует шаблоны и платформы для устранения разрыва между функциональными требованиями приложений и базовыми операционными системами, стеками сетевых протоколов и базами данных

Мидлварь может изменять, расширять или отклонять событие обработки во многих местах конвейера (обработки).

## База

Экземпляр мидлваря можно применить для каждого типа события (update, message, button_pressed etc) в двух местах:

1. Внешняя (outer) область - перед обработкой фильтров (`<router>.<event>.outer_middleware(...)`)
2. Внутренняя (inner) область - после обработки фильтров, но перед обработчиком (`<router>.<event>.middleware(...)`)

<figure markdown>
  ![middleware_light.png](../_static/middleware-light.png#only-light "middleware")
  ![middleware_dark.png](../_static/middleware-dark.png#only-dark "middleware")
  <figcaption>Визуализация порядка обработки</figcaption>
</figure>

!!! warning "Внимание"
    Мидлварь должен быть подклассом `BaseMiddleware` (`#!python from aliceio inport BaseMiddleware`) или поддерживать асинхронный `#!python __call__`.

## Практика

!!! danger "Важно"
    Мидлварь должен всегда вызывать `#!python await handler(event, data)` чтобы передать событие следующему мидлварю/хэндлеру. \
    Если вы хотите завершить обработку события, вы должны не вызывать `#!python await handler(event, data)`

### Class-based

Напишем мидлварь, который будет "разворачивать" незалогиненных в Яндексе пользователей:

```python
from aliceio import BaseMiddleware
from aliceio.types import Update

class UserAuthorizedMiddleware(BaseMiddleware[Update]):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if event.session.user is None:
            logging.info("Замечен пользователь без аккаунта, блокирую!")
            return "Я вас не знаю, у вас нет аккаунта в Яндексе. А чтобы пользоваться мной, он нужен!"
        return await handler(event, data)
```

И теперь добавим его:

```python
dp = Dispatcher()
dp.update.outer_middleware(UserAuthorizedMiddleware())
# либо `dp.update.middleware(UserAuthorizedMiddleware())`
```

### Function-based

Напишем такой же мидлварь через функцию:

```python
@dp.update.middleware()  # либо `@dp.update.outer_middleware()`
async def check_authorization(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any]
) -> Any:
    if event.session.user is None:
        logging.info("Замечен пользователь без аккаунта, блокирую!")
        return "Я вас не знаю, у вас нет аккаунта в Яндексе. А чтобы пользоваться мной, он нужен!"
    return await handler(event, data)
```

## Факты

1. Outer-мидлвари будут вызываться при каждом входящем событиию.
2. Inner-мидлвари будут вызываться только при прохождении фильтров.
3. Если вы ничего не вернёте из мидлваря, то Алиса завершит диалог с навыком.

## Примеры

* [middlewares.py](https://github.com/K1rL3s/aliceio/blob/master/examples/middlewares.py){:target="_blank"}
* [aiogram](https://docs.aiogram.dev/en/dev-3.x/dispatcher/middlewares.html){:target="_blank"}
