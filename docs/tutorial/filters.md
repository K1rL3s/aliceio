# Фильтры

Чтобы не городить сотни if'ов в одном хэндлере, были придуманы фильтры (правила).

Фильтры необходимы для маршрутизации событий конкретным хэндлерам. \
Поиск обработчика всегда останавливается при прохождении первого соответствующего набора фильтров.
По умолчанию все хэндлеры не имеют фильтров, поэтому все события будут передаваться первому обработчику без фильтров.

Основной и самый удобный фильтр - [магический](https://github.com/aiogram/magic-filter){:target="_blank"} `F`-фильтр. \
Пользоваться им крайне легко - просто представьте, что вместо него стоит обрабатываемое событие, и обращайтесь к его атрибутам.

## Кастомный фильтр

Если мы хотим реализовать какую-то сложную проверку (например, с запросом в бд или к какому-то апи), то надо создать свой фильтр.

Фильтры могут быть:

* Асинхронными функциями (`#!python async def my_filter(*args, **kwargs): pass`)
* Синхронными функциями (`#!python def my_filter(*args, **kwargs): pass`)
* Анонимными функциями (`#!python lambda event: True`)
* Любым awaitable объектом
* Подклассом [`aliceio.filters.base.Filter`](../aliceio/filters/base.md){:target="_blank"}
* Экземпляром [`Магического фильтра`](../aliceio/filters/magic-filter.md){:target="_blank"}

И они должны возвращать `bool` или `dict`.
Если возвращается словарь, полученные данные будут переданы следующим фильтрам и обработчику в качестве ключевых аргументов.

Сделаем простой class-based фильтр:

```python
from typing import List
from aliceio.filters import BaseFilter
from aliceio.types import Message

class InWordsFilter(BaseFilter):  # Кастомный фильтр
    def __init__(self, words: List[str]) -> None:
        self.words = words

    async def __call__(self, message: Message) -> bool:
        return message.command in self.words
```

Теперь напишем хэндлеры, которые ловят согласие и отказ - слова "да", "нет" и похожие:

```python
@router.message(InWordsFilter(["да", "ок", "хорошо"]))
async def yes_message_handler(message: Message) -> str:
    return "Ну да так да, чё бубнеть-то"

@router.message(InWordsFilter(["не", "нет", "неа"]))
async def no_message_handler(message: Message) -> str:
    return "Ну на нет и суда нет"
```

## Магический фильтр

Для начала этот фильтр нужно импортировать из aliceio. \
Если импортировать его из magic-filter, то метод `.as_()` не будет доступен
(о нём в главе про [DI](dependency-injection.md){:target="_blank"} и про [магический фильтр](../aliceio/filters/magic-filter.md){:target="_blank"}).

```python
from aliceio import F
```

К уже написанным обработчикам создадим ещё два, которые будут реагировать на [нажатия кнопок с payload'ом](https://yandex.ru/dev/dialogs/alice/doc/request-buttonpressed.html){:target="_blank"}:

```python
# Один и тот же фильтр, но разная запись
@router.button_pressed(F.payload["yes"], F.payload["yes"].is_(True))
async def yes_button_handler(button: ButtonPressed) -> str:
    return "Кнопку нажал? Говорить лень?\nНу да так да, чё бубнеть-то"

# Один и тот же фильтр, но разная запись
@router.button_pressed(~F.payload["yes"], F.payload["yes"].is_(False))
async def no_button_handler(button: ButtonPressed) -> str:
    return"Кнопку нажал? Говорить лень?\nНу на нет и суда нет"
```

И чтобы эти кнопки появились, добавим хэндлер без фильтров, который будет срабатывать всегда, когда событие дойдёт до него:

```python
# Лучше не обрабатывать разные типы событий одним хэндлером
@router.message()
@router.button_pressed()
async def any_message_handler(message: ...) -> Response:
    return Response(
        text="Да-да... Да-да...",
        buttons=[
            TextButton(title="Да", payload={"yes": True}),
            TextButton(title="Нет", payload={"yes": False}),
        ],
    )
```

Допишем обычную точку входа и вуаля, вы прекрасны!

## Комбинация фильтров

Есть два основных способа комбинации фильтров: "и" и "или".
Все фильтры можно комбинировать друг с другом и создавать любые конфигурации под любую задачу.

### Логическое "и"

Предпочтительный:
```python
@<router>.message(F.text.startswith("yoy"), F.text.endswith("wasap?"))
```

Дополнительный (с помощью `and_f()` фильтра):
```python
@<router>.message(and_f(F.text.startswith("yoy"), F.text.endswith("wasap?")))
```

### Логическое "или"

Предпочтительный:
```python
@<router>.message(F.text.startswith("yoy"))
@<router>.message(F.text.endswith("wasap?"))
```

Дополнительный (с помощью `or_f()` фильтра):
```python
@<router>.message(or_f(F.text.startswith("yoy"), F.text.endswith("wasap?")))
```

### Логическое "не" (инверсия)

Предпочтительный:
```python
@<router>.message(~F.text.startswith("yoy"))
```

Дополнительный (с помощью `invert_f()` фильтра):
```python
@<router>.message(invert_f(F.text.startswith("yoy")))
```

## Примеры

* [filters.py](https://github.com/K1rL3s/aliceio/blob/master/examples/filters.py){:target="_blank"}
* [aiogram](https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/index.html){:target="_blank"}
* [aiogram-magic](https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html){:target="_blank"}
