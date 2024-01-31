# Методы API

Чтобы получить, загрузить и удалить загруженные изображения и звуки, надо передать [OAuth Token](https://yandex.ru/dev/direct/doc/start/token.html) при создании навыка и воспользоваться одним из следующих методов экземпляра:

!!! warning
    Без токена невозможно использовать все следующие методы.

# Свободное место

## ::: aliceio.client.skill.Skill.status
    handler: python
    options:
      show_source: false

Для каждого аккаунта Яндекса на Диалоги можно загрузить не больше 100 МБ картинок и 1 ГБ аудио. Чтобы узнать, сколько места уже занято, используйте этот метод.
[Док 1](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__quota)
[Док 2](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__quota)


# Изображения

## ::: aliceio.client.skill.Skill.get_images
    handler: python
    options:
      show_source: false

Список изображений, загруженных для навыка, можно получить этим методом. [Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__list)

## ::: aliceio.client.skill.Skill.upload_image
    handler: python
    options:
      show_source: false


Чтобы загрузить картинку из для навыка из интернета, передайте URL картинки в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__download-internet)

Чтобы загрузить файл, передайте наследника `InputFile`'а в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__upload-file)

## ::: aliceio.client.skill.Skill.delete_image
    handler: python
    options:
      show_source: false

Чтобы удалить загруженное изображение, передайте его идентификатор в этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-upload.html#http-images-load__delete)


# Аудио

## ::: aliceio.client.skill.Skill.get_sounds
    handler: python
    options:
      show_source: false

Чтобы посмотреть аудиофайлы, загруженные для навыка, используйте этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__list)

## ::: aliceio.client.skill.Skill.upload_sound
    handler: python
    options:
      show_source: false

Аудио можно загрузить только файлом, передайте наследника `InputFile`'а в метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__upload-file)

## ::: aliceio.client.skill.Skill.delete_sound
    handler: python
    options:
      show_source: false

Чтобы удалить загруженное аудио, передайте его идентификатор в этот метод.
[Док](https://yandex.ru/dev/dialogs/alice/doc/resource-sounds-upload.html#http-load__delete)


# Примеры

* [methods.py](https://ya.ru)
