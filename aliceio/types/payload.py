from typing import Any

Payload = dict[str, Any]
# Произвольный JSON-объект, который Яндекс Диалоги должны отправить обработчику,
# если данная кнопка будет нажата.
# Максимум 4096 байт.
# https://yandex.ru/dev/dialogs/alice/doc/ru/request-buttonpressed#request-desc
