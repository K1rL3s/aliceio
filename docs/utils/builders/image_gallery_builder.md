# Класс ImageGalleryBuilder
`ImageGalleryBuilder(Builder[ImageGallery, ImageGalleryItem]):` - Билдер галереи (альбомов) изображений.
### Параметры

`self._items: List[ImageGalleryItem] = []`

### Функции

- `add(self, item: Union[ImageGalleryItem, str], /, title: Optional[str] = None, button: Optional[MediaButton] = None,) -> Self:`\
Добавить айтем в билдер.
    ```
    @overload
    add(self, image_id: str, /, title: Optional[str] = None, button: Optional[MediaButton] = None,) -> Self:
    add(self, item: ImageGalleryItem, /) -> Self:
    ```

- `to_collection(self) -> ImageGallery:` - Создать коллекцию из текущего билдера.
