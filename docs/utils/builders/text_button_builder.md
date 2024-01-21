# Класс TextButtonsBuilder
`TextButtonsBuilder(Builder[List[TextButton], TextButton]):` - Билдер текстовых кнопок.
### Параметры

`self._items: List[TextButton] = []`

### Функции

- `add(self, item: Union[TextButton, str], /, url: Optional[str] = None, payload: Optional[Payload] = None, hide: bool = True,) -> Self:`\
Добавить айтем в билдер.
    ```
    @overload
    add(self, title: str, /, url: Optional[str] = None, payload: Optional[Payload] = None, hide: bool = True,) -> Self:
    add(self, item: TextButton, /) -> Self:
    ```

- `to_collection(self) -> List[TextButton]:` - Создать коллекцию из текущего билдера.
