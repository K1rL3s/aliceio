## Payload

Произвольный [JSON-объект](https://yandex.ru/dev/dialogs/alice/doc/request-buttonpressed.html#request-buttonpressed__request-desc), который Яндекс Диалоги должны отправить обработчику, если данная кнопка будет нажата.

Максимум 4096 байт.

```python
from typing import Any, Dict

Payload = Dict[str, Any]
```
