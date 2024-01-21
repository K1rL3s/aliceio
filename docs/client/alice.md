# Класс AliceAPIServer
`AliceAPIServer` - Базовый конфиг для энподинтов API Алисы.

### Параметры

`base: str`\
`file: str`

### Функции
- `api_url(self, method: str) -> str:`\
Генерирует URL для независящих от навыка методов API Алисы (например, status).


- `upload_file_url(self, skill_id: str, file_type: str) -> str:`\
Генерирует URL для загрузки файла на сервер API Алисы.


- `get_file_url(self, skill_id: str, file_type: str, file_id: str) -> str:`\
Генерирует URL для получения информации о файле на сервере API Алисы.


- `get_all_files_url(self, skill_id: str, file_type: str) -> str:`\
Генерирует URL для получения информации о всех файлах на сервере API Алисы.


- `delete_file_url(self, skill_id: str, file_type: str, file_id: str) -> str:`\
Генерирует URL для удаления файла с сервера API Алисы.


- `from_base(cls, base: str) -> "AliceAPIServer":`\
Используйте этот метод для автогенерации AliceAPIServer из базового URL.



```PRODUCTION = AliceAPIServer.from_base(base="https://dialogs.yandex.net/api/v1/")```
