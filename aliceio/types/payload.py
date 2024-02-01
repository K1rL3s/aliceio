from typing import Any, Dict

Payload = Dict[str, Any]
# Произвольный JSON-объект, который Яндекс Диалоги должны отправить обработчику,
# если данная кнопка будет нажата.
# Максимум 4096 байт.
# https://yandex.ru/dev/dialogs/alice/doc/request-buttonpressed.html#request-buttonpressed__request-desc
