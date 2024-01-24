# Класс Skill
`Skill` - Класс навыка
### Параметры

`skill_id: str`\
Идентификатор навыка можно посмотреть в консоли разработчика.\
Зайдите на страницу навыка, откройте вкладку "Общие сведения"
и пролистайте вниз. Запросы без этого айди будут игнорироваться.\
`oauth_token: Optional[str] = None`\
[Токен](https://yandex.ru/dev/direct/doc/start/token.html) для загрузки аудио и изображений. 
Без этого токена нельзя взаимодействовать с API Алисы.\
`session: Optional[BaseSession] = None`\
HTTP Client session (Например, AiohttpSession).\
Если не указано, будет создано автоматически.
### Функции
- `__eq__(self, other: Any):`\
Сравнить текущий навык с другим экземпляром навыка.


- `__call__(self, method: AliceMethod[T], request_timeout: Optional[int] = None,) -> T:`\
Вызов API Алисы.


- `status(self, request_timeout: Optional[int] = None) -> SpaceStatus:`\
Вызывает метод `:class:Status` <ссылка на доку>

##### @property
- `token` - Возвращает токен навыка.
- `oauth_token` - Возвращает токен навыка.
- `skill_id` - Возвращает айди навыка.
- `id` - Возвращает айди навыка.

###### @asynccontextmanager
Использование в контекстном менеджере.
- `context(self, auto_close: bool = True) -> AsyncIterator[Skill]`\
`:param auto_close:` - Закрыть ли HTTP-сессию при выходе.\
Возвращает класс `Skill`

#### get/upload/delete_image

- `get_images(self, request_timeout: Optional[int] = None,) -> UploadedImagesList:`
Вызывает метод `:class:GetImages` <ссылка на доку>


- `upload_image(self, file: Union[InputFile, str], request_timeout: Optional[int] = None,) -> PreUploadedImage:`\
Вызывает метод `:class:UploadImage` <ссылка на доку>

    ```
    @overload
    upload_image(self, url: str, /, request_timeout: Optional[int] = None,) -> PreUploadedImage:
    
    @overload
    upload_image(self, file: Union[InputFile, str], /, request_timeout: Optional[int] = None,) -> PreUploadedImage:
    ```

- `delete_image(self, file_id: str, request_timeout: Optional[int] = None,) -> Result:`\
Вызывает метод `:class:DeleteImage` <ссылка на доку>


#### get/upload/delete_sound

- `get_sounds(self, request_timeout: Optional[int] = None,) -> UploadedSoundsList:`\
Вызывает метод `:class:GetSounds` <ссылка на доку>


- `upload_sound(self, file: InputFile, request_timeout: Optional[int] = None,) -> PreUploadedSound:`\
Вызывает метод `:class:UploadSound` <ссылка на доку>


- `delete_sound(self, file_id: str, request_timeout: Optional[int] = None,) -> Result:`\
Вызывает метод `:class:DeleteSound` <ссылка на доку>
