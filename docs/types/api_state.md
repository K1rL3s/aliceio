## [Хранение состояния](https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html)

```python
from typing import Any, Dict

StateDict = Dict[str, Any]
SessionState = StateDict
AuthorizedUserState = StateDict
ApplicationState = StateDict
```

::: aliceio.types.api_state.ApiState
    handler: python
    options:
      members: true
