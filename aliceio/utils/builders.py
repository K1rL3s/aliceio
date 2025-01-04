from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, Union, overload

from typing_extensions import Self

from aliceio.types import (
    CardFooter,
    CardHeader,
    ImageGallery,
    ImageGalleryItem,
    ItemImage,
    ItemsList,
    MediaButton,
    Payload,
    TextButton,
)

Collection = TypeVar("Collection", ItemsList, ImageGallery, list[TextButton])
Item = TypeVar("Item", ItemImage, ImageGalleryItem, TextButton)


class Builder(ABC, Generic[Collection, Item]):
    """Базовый класс билдера"""

    _items: list[Item]

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, item: Item) -> Self:
        """Добавить айтем в билдер."""

    @abstractmethod
    def to_collection(self) -> Collection:
        """Создать коллекцию из текущего билдера."""

    def __len__(self) -> int:
        """Узнать длину коллекции."""
        return len(self._items)


class ItemsListBuilder(Builder[ItemsList, ItemImage]):
    """Билдер элементов списка."""

    def __init__(self) -> None:
        self._items: list[ItemImage] = []
        self._header: Optional[CardHeader] = None
        self._footer: Optional[CardFooter] = None

    @overload
    def add(
        self,
        image_id: str,
        /,
        title: Optional[str] = None,
        description: Optional[str] = None,
        button: Optional[MediaButton] = None,
    ) -> Self: ...

    @overload
    def add(self, item: ItemImage, /) -> Self: ...

    def add(
        self,
        item: Union[ItemImage, str],
        /,
        title: Optional[str] = None,
        description: Optional[str] = None,
        button: Optional[MediaButton] = None,
    ) -> Self:
        if isinstance(item, str):
            item = ItemImage(
                image_id=item,
                title=title,
                description=description,
                button=button,
            )
        self._items.append(item)
        return self

    @overload
    def set_header(self, text: str, /) -> Self: ...

    @overload
    def set_header(self, header: CardHeader, /) -> Self: ...

    def set_header(self, header: Union[CardHeader, str], /) -> Self:
        if isinstance(header, str):
            header = CardHeader(text=header)
        self._header = header
        return self

    @overload
    def set_footer(
        self,
        text: str,
        /,
        button: Optional[MediaButton] = None,
    ) -> Self: ...

    @overload
    def set_footer(self, footer: CardFooter, /) -> Self: ...

    def set_footer(
        self,
        footer: Union[CardFooter, str],
        /,
        button: Optional[MediaButton] = None,
    ) -> Self:
        if isinstance(footer, str):
            footer = CardFooter(text=footer, button=button)
        self._footer = footer
        return self

    def to_collection(self) -> ItemsList:
        """Возвращает список элементов."""
        return ItemsList(
            items=self._items.copy(),
            header=self._header.model_copy() if self._header else None,
            footer=self._footer.model_copy() if self._footer else None,
        )


class ImageGalleryBuilder(Builder[ImageGallery, ImageGalleryItem]):
    def __init__(self) -> None:
        self._items: list[ImageGalleryItem] = []

    @overload
    def add(
        self,
        image_id: str,
        /,
        title: Optional[str] = None,
        button: Optional[MediaButton] = None,
    ) -> Self: ...

    @overload
    def add(self, item: ImageGalleryItem, /) -> Self: ...

    def add(
        self,
        item: Union[ImageGalleryItem, str],
        /,
        title: Optional[str] = None,
        button: Optional[MediaButton] = None,
    ) -> Self:
        if isinstance(item, str):
            item = ImageGalleryItem(image_id=item, title=title, button=button)
        self._items.append(item)
        return self

    def to_collection(self) -> ImageGallery:
        return ImageGallery(items=self._items.copy())


class TextButtonsBuilder(Builder[list[TextButton], TextButton]):
    def __init__(self) -> None:
        self._items: list[TextButton] = []

    @overload
    def add(
        self,
        title: str,
        /,
        url: Optional[str] = None,
        payload: Optional[Payload] = None,
        hide: bool = True,
    ) -> Self: ...

    @overload
    def add(self, item: TextButton, /) -> Self: ...

    def add(
        self,
        item: Union[TextButton, str],
        /,
        url: Optional[str] = None,
        payload: Optional[Payload] = None,
        hide: bool = True,
    ) -> Self:
        if isinstance(item, str):
            item = TextButton(
                title=item,
                url=url,
                payload=payload,
                hide=hide,
            )
        self._items.append(item)
        return self

    def to_collection(self) -> list[TextButton]:
        return self._items.copy()
