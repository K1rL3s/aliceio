# Класс ItemsListBuilder
`ItemsListBuilder(Builder[ItemsList, ItemImage])` - Билдер элементов списка.

### Параметры

- `self._items: List[ItemImage] = []`
- `self._header: Optional[CardHeader] = None`
- `self._footer: Optional[CardFooter] = None`

### Функции

- `add(self, item: Union[ItemImage, str], /, title: Optional[str] = None, description: Optional[str] = None, button: Optional[MediaButton] = None,) -> Self`\
Добавить айтем в билдер.
  ```
  @overload
  add(self, image_id: str, /,title: Optional[str] = None,description: Optional[str] = None,button: Optional[MediaButton] = None,) -> Self
  add(self, item: ItemImage, /) -> Self
  ```
- `set_header(self, header: Union[CardHeader, str], /) -> Self`
  ```
  @overload
  set_header(self, text: str, /) -> Self
  set_header(self, header: CardHeader, /) -> Self
  ```

- `set_footer(self, footer: Union[CardFooter, str], /, button: Optional[MediaButton] = None,) -> Self`
    ```
    @overload
    set_footer(self, text: str, /, button: Optional[MediaButton] = None) -> Self
    set_footer(self, footer: CardFooter, /) -> Self
    ```
