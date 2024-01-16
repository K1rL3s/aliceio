import pytest
from pydantic import ValidationError

from aliceio.types import (
    CardFooter,
    CardHeader,
    ImageGallery,
    ImageGalleryItem,
    ItemImage,
    ItemsList,
    MediaButton,
    TextButton,
)
from aliceio.utils.builders import (
    ImageGalleryBuilder,
    ItemsListBuilder,
    TextButtonsBuilder,
)


class TestItemsListBuilder:
    def test_add_item_and_return_self(self):
        builder = ItemsListBuilder()

        item = ItemImage(image_id="1", title="Item 1", description="Description 1")

        assert builder.add(item) == builder
        assert builder.add("image_id") == builder

    def test_set_header_and_return_self(self):
        builder = ItemsListBuilder()

        header = CardHeader(text="text")

        assert builder.set_header(header) == builder
        assert builder.set_header("text") == builder

    def test_set_footer_and_return_self(self):
        builder = ItemsListBuilder()

        footer = CardFooter(text="text")

        assert builder.set_footer(footer) == builder
        assert builder.set_footer("text") == builder

    def test_set_item(self):
        builder = ItemsListBuilder()
        item = ItemImage(
            image_id="id",
            title="title",
            description="description",
            button=MediaButton(text="text", url="url"),
        )

        builder.add(item)

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], ItemImage)
        assert builder._items[0].image_id == "id"
        assert builder._items[0].title == "title"
        assert builder._items[0].description == "description"
        assert builder._items[0].button.text == "text"
        assert builder._items[0].button.url == "url"

    def test_set_item_from_item_image_args(self):
        builder = ItemsListBuilder()

        builder.add(
            "id",
            title="title",
            description="description",
            button=MediaButton(text="text", url="url"),
        )

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], ItemImage)
        assert builder._items[0].image_id == "id"
        assert builder._items[0].title == "title"
        assert builder._items[0].description == "description"
        assert builder._items[0].button.text == "text"
        assert builder._items[0].button.url == "url"

    def test_set_header(self):
        builder = ItemsListBuilder()
        header = CardHeader(text="text")

        builder.set_header(header)

        assert isinstance(builder._header, CardHeader)
        assert builder._header.text == "text"

    def test_set_header_from_str(self):
        builder = ItemsListBuilder()

        builder.set_header("text")

        assert isinstance(builder._header, CardHeader)
        assert builder._header.text == "text"

    def test_set_footer(self):
        builder = ItemsListBuilder()
        footer = CardFooter(text="text", button=MediaButton(text="text", url="url"))

        builder.set_footer(footer)

        assert isinstance(builder._footer, CardFooter)
        assert builder._footer.text == "text"
        assert builder._footer.button.text == "text"
        assert builder._footer.button.url == "url"

    def test_set_footer_from_str_and_button(self):
        builder = ItemsListBuilder()

        builder.set_footer("test", MediaButton(text="text", url="url"))

        assert isinstance(builder._footer, CardFooter)
        assert builder._footer.text == "test"
        assert builder._footer.button.text == "text"
        assert builder._footer.button.url == "url"

    def test_cant_build_without_items(self):
        builder = ItemsListBuilder()

        with pytest.raises(ValidationError):
            builder.to_collection()

    def test_cant_build_with_more_than_5_items(self):
        builder = ItemsListBuilder()
        for _ in range(5):
            builder.add("id")

        assert len(builder._items) == len(builder) == 5
        assert isinstance(builder.to_collection(), ItemsList)

        builder.add("id")
        assert len(builder._items) == len(builder) == 6

        with pytest.raises(ValueError):
            builder.to_collection()


class TestImageGalleryBuilder:
    def test_add_item_and_return_self(self):
        builder = ImageGalleryBuilder()

        item = ImageGalleryItem(image_id="image_id")
        assert builder.add(item) == builder

        assert builder.add("image_id") == builder

    def test_add_item(self):
        builder = ImageGalleryBuilder()
        item = ImageGalleryItem(
            image_id="id",
            title="title",
            button=MediaButton(text="text", url="url"),
        )

        builder.add(item)

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], ImageGalleryItem)
        assert builder._items[0].image_id == "id"
        assert builder._items[0].title == "title"
        assert builder._items[0].button.text == "text"
        assert builder._items[0].button.url == "url"

    def test_add_item_from_item_args(self):
        builder = ImageGalleryBuilder()

        builder.add(
            "id",
            title="title",
            button=MediaButton(text="text", url="url"),
        )

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], ImageGalleryItem)
        assert builder._items[0].image_id == "id"
        assert builder._items[0].title == "title"
        assert builder._items[0].button.text == "text"
        assert builder._items[0].button.url == "url"

    def test_cant_build_without_items(self):
        builder = ImageGalleryBuilder()

        with pytest.raises(ValidationError):
            builder.to_collection()

    def test_cant_build_with_more_than_10_items(self):
        builder = ImageGalleryBuilder()
        for _ in range(10):
            builder.add("image_id")

        assert len(builder._items) == len(builder) == 10
        assert isinstance(builder.to_collection(), ImageGallery)

        builder.add("image_id")
        assert len(builder._items) == len(builder) == 11

        with pytest.raises(ValidationError):
            builder.to_collection()


class TestTextButtonsBuilder:
    def test_add_item_and_return_self(self):
        builder = TextButtonsBuilder()

        item = TextButton(title="title")

        assert builder.add(item) == builder

    def test_add_item(self):
        builder = TextButtonsBuilder()
        item = TextButton(title="title", url="url", hide=False, payload={"k": "v"})

        builder.add(item)

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], TextButton)
        assert builder._items[0].title == "title"
        assert builder._items[0].url == "url"
        assert builder._items[0].hide is False
        assert builder._items[0].payload == {"k": "v"}

    def test_add_item_from_item_args(self):
        builder = TextButtonsBuilder()

        builder.add("title", url="url", payload={"k": "v"}, hide=False)

        assert len(builder._items) == len(builder) == 1
        assert isinstance(builder._items[0], TextButton)
        assert builder._items[0].title == "title"
        assert builder._items[0].url == "url"
        assert builder._items[0].hide is False
        assert builder._items[0].payload == {"k": "v"}

    def test_can_build_without_items(self):
        builder = TextButtonsBuilder()

        assert isinstance(builder.to_collection(), list)
