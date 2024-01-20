# Класс Skill
`Skill` - Класс навыка
### Параметры
```
:param skill_id: str
:param oauth_token: Optional[str] = None
:param session: Optional[BaseSession] = None
```
`skill_id:`\
Идентификатор навыка можно посмотреть в консоли разработчика.\
Зайдите на страницу навыка, откройте вкладку "Общие сведения"
и пролистайте вниз. Запросы без этого айди будут игнорироваться.\
`oauth_token:`\
[Токен](https://yandex.ru/dev/direct/doc/start/token.html) для загрузки аудио и изображений. 
Без этого токена нельзя взаимодействовать с API Алисы.\
`session:`\
HTTP Client session (Например, AiohttpSession).\
Если не указано, будет создано автоматически.
### Функции
- `__eq__(self, other: Any):`\
Сравнить текущий навык с другим экземпляром навыка.\


- `__call__(self, method: AliceMethod[T], request_timeout: Optional[int] = None,) -> T:` - Вызов API Алисы.\
`:param method:` Запрос, наследник :code:`AliceMethod`


- `status(self, request_timeout: Optional[int] = None) -> SpaceStatus:`\
`:return: self(status, request_timeout=request_timeout)`

#### @property
- `token` - Возвращает токен навыка.\
- `oauth_token` - Возвращает токен навыка.\
- `skill_id` - Возвращает айди навыка.\
- `id` - Возвращает айди навыка.

#### @asynccontextmanager
Использование в контекстном менеджере.
- `context(self, auto_close: bool = True) -> AsyncIterator[Skill]`\
`:param auto_close:` - Закрыть ли HTTP-сессию при выходе.\
`:return:` - Skill

#### get/upload/delete_image
```
get_images(self, request_timeout: Optional[int] = None,) -> UploadedImagesList:
:return: self(get_images, request_timeout=request_timeout)


@overload
upload_image(self, url: str, /, request_timeout: Optional[int] = None,) -> PreUploadedImage:
:return: pass

@overload
upload_image(self, file: Union[InputFile, str], /, request_timeout: Optional[int] = None,) -> PreUploadedImage:
:return: pass

upload_image(self, file: Union[InputFile, str], request_timeout: Optional[int] = None,) -> PreUploadedImage:
:return: self(upload_image, request_timeout=request_timeout)


delete_image(self, file_id: str, request_timeout: Optional[int] = None,) -> Result:
:return: self(get_sounds, request_timeout=request_timeout)
```

#### get/upload/delete_sound
```
get_sounds(self, request_timeout: Optional[int] = None,) -> UploadedSoundsList:
:return: self(get_sounds, request_timeout=request_timeout)

upload_sound(self, file: InputFile, request_timeout: Optional[int] = None,) -> PreUploadedSound:
:return: self(upload_sound, request_timeout=request_timeout)

delete_sound(self, file_id: str, request_timeout: Optional[int] = None,) -> Result:
:return: self(delete_sound, request_timeout=request_timeout)
```
