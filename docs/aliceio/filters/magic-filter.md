# Магический фильтр

!!! note "Примечание"
    В aliceio есть небольшая надстройка над магическим фильтром.
    Если импортировать его из [magic-filter](https://pypi.org/project/magic-filter/){:target="_blank"}, то метод `.as_()` не будет доступен (о нём в главе про DI).

`MagicFilter` можно вызвать как функцию, он поддерживает некоторые действия и запоминает цепочку атрибутов и действий, которые следует проверить.

Это означает, что вы можете связать методы получения атрибутов в цепочку, описать простые проверки данных, а затем вызвать полученный объект, передав один объект в качестве аргумента.
Например, можно создать цепочку атрибутов `F.foo.bar.baz`, затем добавить действие `F.foo.bar.baz == 'spam'`, а затем вызвать полученный объект `(F.foo.bar.baz == 'spam').resolve(obj)`

### Возможные действия

Магический фильтр поддерживает некоторые логические операции над атрбитуами объекта.

#### Существует ли
```python
F.text  # эквивалент `lambda message: message.text`
```

#### Входит ли в коллекцию
```python
F.from_user.id.in_({42, 1000, 123123})  # lambda event: event.from_user.id in {42, 1000, 123123}
F.event_type.in_({'foo', 'bar', 'baz'})  # lambda update: update.event_type in {'foo', 'bar', 'baz'}
```

#### Содержит ли
```python
F.text.contains('foo')  # lambda message: 'foo' in message.text
```

#### Regexp
```python
F.text.regexp(r'Hello, .+')  # lambda message: re.match(r'Hello, .+', message.text)
```

#### Свои функции

Принимает любой вызываемый объект. Объект будет вызван когда фильтр проверяет результат.
```python
F.chat.func(lambda chat: chat.id == -42)  # lambda message: (lambda chat: chat.id == -42)(message.chat)
```

#### Инверсия
Любая доступная операция может быть инвертирована с помощью оператора `~`
```python
~(F.text == 'spam')  # lambda message: message.text != 'spam'
~F.text.startswith('spam')  # lambda message: not message.text.startswith('spam')
```

#### Комбинация
Все операции могут быть скомбинированы с помощью `&`и `|`
```python
(F.from_user.id == 42) & (F.text == 'admin')
F.text.startswith('a') | F.text.endswith('b')
(F.from_user.id.in_({42, 777, 911})) & (F.text.startswith('!') | F.text.startswith('/')) & F.text.contains('ban')
```

#### Строковые методы
Могут быть использованы только с строковыми атрибутами
```python
F.text.startswith('foo')  # lambda message: message.text.startswith('foo')
F.text.endswith('bar')  # lambda message: message.text.startswith('bar')
F.text.lower() == 'test'  # lambda message: message.text.lower() == 'test'
F.text.upper().in_({'FOO', 'BAR'})  # lambda message: message.text.upper() in {'FOO', 'BAR'}
F.text.len() == 5  # lambda message: len(message.text) == 5
```

### Использование в aliceio
```python
@router.message(F.text == "привет")
@router.button_pressed(F.payload["yes"])
...
```

::: aliceio.utils.magic_filter.MagicFilter
    handler: python
    options:
      members: true

<br/>

::: aliceio.utils.magic_filter.AsFilterResultOperation
    handler: python
    options:
      members: true
