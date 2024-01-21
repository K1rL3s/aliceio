# Класс Builder
`Builder(ABC, Generic[Collection, Item])` - Билдер объектов клавиатуры.
### Параметры

`_items: List[Item]`

### Функции
- `__len__(self) -> int:` - Возвращает длину коллекции.


#### @abstractmethod
- `add` - Добавить айтем в билдер.
- `to_collection` - Создать коллекцию из текущего билдера.
