# Машина состояний

> Finite-state machine (FSM) или finite-state automation (FSA), конечный автомат — это математическая модель вычислений.
>
> Это абстрактная машина, которая в любой момент времени может находиться ровно в одном из конечного числа состояний. Конечный автомат может переходить из одного состояния в другое в ответ на некоторые входные данные; переход из одного состояния в другое называется переходом.
>
> Конечный автомат определяется списком его состояний, его начальным состоянием и входными данными, которые запускают каждый переход.
>
> <cite>[Википедия](https://en.wikipedia.org/wiki/Finite-state_machine)</cite>

## Проблема

Не вся функциональность навыка может быть реализована в одном хэндлере.
Если вам нужно получить некоторую информацию от пользователя в несколько шагов или нужно направить его в зависимости от ответа, то вам надо использовать FSM.

Посмотрим, как это сделать пошагово.

## Решение

Перед обработкой любый состояний вы должны определить какие именно состояния вы хотите использовать:

```python
class Form(StatesGroup):
    name = State()
    like_skills = State()
    device = State()
```

И теперь напишите хэндлер для каждого состояния отдельно от старта диалога.

Диалоги начинаются с новой сессией, поэтому давайте поймаем это и переместим пользователя в состояние `Form.name`:

```python
@form_router.message(F.session.new)
async def new_session(message: Message, state: FSMContext) -> str:
    await state.set_state(Form.name)
    return "Привет! Как тебя зовут?"
```

После этого вы должны сохранить эти данные в хранилище и переместить пользователя в следующее состояние:

```python
@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> Response:
    await state.update_data(name=message.command)
    await state.set_state(Form.like_skills)
    return Response(
        text=f"Рад познакомиться, {message.command}!\nТебе нравятся навыки Алисы?",
        buttons=[
            TextButton(title="Да"),
            TextButton(title="Нет"),
        ],
    )
```

На следующих этапах пользователь может дать разные ответы, например, это может быть *да*, *нет* или что-то другое.

Обработаем `да` и поставим состояние `Form.device`:

```python
@form_router.message(Form.like_skills, F.command == "да")
async def process_like_skills(message: Message, state: FSMContext) -> Response:
    await state.set_state(Form.device)
    return Response(
        text="Класс! Мне тоже!\nЧерез какое устройство ты обычно их используешь?"
    )
```

Обработаем `нет`:

```python
@form_router.message(Form.like_skills, F.command == "нет")
async def process_dont_like_skills(message: Message, state: FSMContext) -> Response:
    data = await state.get_data()
    await state.clear()
    return Response(
        text="Ну, бывает.\n" + show_summary(data=data, positive=False),
        end_session=True,
    )
```

И все остальные случаи:

```python
@form_router.message(Form.like_skills)
async def process_unknown_write_skills(message: Message) -> Response:
    return Response(
        text="Не могу понять тебя... Можешь повторить, пожалуйста?",
        buttons=[
            TextButton(title="Да"),
            TextButton(title="Нет"),
        ],
    )
```

Все возможные случаи шага *Form.like_skills* были рассмотрены, давайте реализуем последний шаг:

```python
@form_router.message(Form.device)
async def process_device(message: Message, state: FSMContext) -> Response:
    data = await state.update_data(device=message.command)
    await state.clear()

    if message.command == "телефон":
        text = "С телефона? Да, это самое удобное, с чего можно пользоваться Алисой.\n"
    else:
        text = ""
    text += show_summary(data=data)

    return Response(text=text, end_session=True)
```
```python
def show_summary(data: Dict[str, Any], positive: bool = True) -> str:
    name = data["name"]
    device = data.get("device", "чём-то непонятном")
    text = f"Я буду помнить, {name}, что "
    text += (
        f"тебе нравятся навыки Алисы на {device}."
        if positive
        else "тебе не нравятся навыки Алисы..."
    )
    return text
```

Теперь, когда мы доделали диалог, надо сделать возможность отменить разговор:

```python
@form_router.message(F.command == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> Response:
    """Позволяет пользователю отменить любое действие."""
    current_state = await state.get_state()
    if current_state is not None:
        logging.info("Cancelling state %r", current_state)
        await state.clear()

    return Response(text="Окей, стою. Пока-пока!", end_session=True)
```

Готово!

## Примеры

* [finite_state_machine.py](https://github.com/K1rL3s/aliceio/blob/master/examples/finite_state_machine.py)
* [aiogram](https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/index.html)
