# Класс BaseSession
`BaseSession(abc.ABC)` - Базовый класс для всех HTTP-сессий в aliceio.\
Если вы хотите создать свою собственную сессию, вы должны наследовать этот класс.
## Параметры

`api: AliceAPIServer = PRODUCTION` - URL паттерны API Алисы.\
`json_loads: _JsonLoads = json.loads` - JSON Loads.\
`json_dumps: _JsonDumps = json.dumps` - Json Dumps.\
`timeout: float = DEFAULT_TIMEOUT` - Тайм-аут запроса сессии.

## Функции
- `check_response(self, skill: Skill, method: AliceMethod[AliceType], status_code: int, content: str,) -> Response[AliceType]:`\
Проверка статуса ответа.


- `close(self) -> None:`\
Закрыть клиентскую сессию.


- `make_request(self, skill: Skill, method: AliceMethod[AliceType], timeout: Optional[int] = None,) -> AliceType:`\
Запрос к API Алисы.


- `prepare_value(self, value: Any, skill: Skill, files: Dict[str, Any], _dumps_json: bool = False,) -> Any:`\
Подготовка значения перед отправкой.
