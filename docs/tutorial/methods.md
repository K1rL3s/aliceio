# Методы API

Чтобы получить, загрузить и удалить загруженные изображения и звуки, надо передать [OAuth Token](https://yandex.ru/dev/direct/doc/start/token.html){:target="_blank"} при создании навыка и воспользоваться одним из следующих методов экземпляра:

```python
skill = Skill(skill_id="...", oauth_token="it_is_required_for_methods")
```

!!! warning "Предупреждение"
    Без токена невозможно использовать все следующие методы.

## Свободное место

### ::: aliceio.client.skill.Skill.status
    handler: python
    options:
      show_source: false

Для каждого аккаунта Яндекса на Диалоги можно загрузить не больше 100 МБ картинок и 1 ГБ аудио. Чтобы узнать, сколько места уже занято, используйте этот метод.
[Док 1](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__quota){:target="_blank"}
[Док 2](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__quota){:target="_blank"}

```python
space_status = await skill.status()
```

## Изображения

### ::: aliceio.client.skill.Skill.get_images
    handler: python
    options:
      show_source: false

Список изображений, загруженных для навыка, можно получить этим методом. [Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__list){:target="_blank"}

```python
images = await skill.get_images()
```

### ::: aliceio.client.skill.Skill.upload_image
    handler: python
    options:
      show_source: false


Чтобы загрузить картинку для навыка из интернета, передайте URL картинки в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__download-internet){:target="_blank"}

```python
image = await skill.upload_image("https://example.com")
```

Чтобы загрузить файл, передайте наследника `InputFile`'а в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__upload-file){:target="_blank"}

```python
image = await skill.upload_image(BufferedInputFile(file=b"..."))
```

### ::: aliceio.client.skill.Skill.delete_image
    handler: python
    options:
      show_source: false

Чтобы удалить загруженное изображение, передайте его идентификатор в этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__delete){:target="_blank"}

```python
result = await skill.delete_image(file_id="...")
```

## Аудио

### ::: aliceio.client.skill.Skill.get_sounds
    handler: python
    options:
      show_source: false

Чтобы посмотреть аудиофайлы, загруженные для навыка, используйте этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__list){:target="_blank"}

```python
sounds = await skill.get_sounds()
```

### ::: aliceio.client.skill.Skill.upload_sound
    handler: python
    options:
      show_source: false

Аудио можно загрузить только файлом, передайте наследника `InputFile`'а в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__upload-file){:target="_blank"}

```python
sound = await skill.upload_sound(path="...")
```

### ::: aliceio.client.skill.Skill.delete_sound
    handler: python
    options:
      show_source: false

Чтобы удалить загруженное аудио, передайте его идентификатор в этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__delete){:target="_blank"}

```python
result = await skill.delete_sound(file_id="...")
```

## Примеры

* [methods.py](https://github.com/K1rL3s/aliceio/blob/master/examples/methods.py){:target="_blank"}
