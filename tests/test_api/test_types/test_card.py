import pytest
from pydantic import ValidationError

from aliceio.enums.card import CardType
from aliceio.exceptions import AliceWrongFieldError
from aliceio.types import BigImage, ImageGallery, ImageGalleryItem, ItemImage, ItemsList


class TestBigImage:
    @pytest.mark.parametrize(
        "card_type",
        ["test", 42, None, CardType.ITEMS_LIST, CardType.IMAGE_GALLERY],
    )
    def test_wrong_type(self, card_type: str) -> None:
        if isinstance(card_type, str):
            with pytest.raises(AliceWrongFieldError):
                BigImage(image_id="42:IMAGE_ID", type=card_type)
        else:
            with pytest.raises(ValidationError):
                BigImage(image_id="42:IMAGE_ID", type=card_type)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.BIG_IMAGE, "bigimage", "BIGIMAGE"],
    )
    def test_good_type(self, card_type: str) -> None:
        BigImage(image_id="42:IMAGE_ID", type=card_type)


class TestItemsList:
    @pytest.mark.parametrize(
        "card_type",
        ["test", 42, None, CardType.BIG_IMAGE, CardType.IMAGE_GALLERY],
    )
    def test_wrong_type(self, card_type: str) -> None:
        items = [ItemImage(image_id="id")]
        if isinstance(card_type, str):
            with pytest.raises(AliceWrongFieldError):
                ItemsList(type=card_type, items=items)
        else:
            with pytest.raises(ValidationError):
                ItemsList(type=card_type, items=items)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.ITEMS_LIST, "itemslist", "ITEMSLIST"],
    )
    def test_good_type(self, card_type: str) -> None:
        ItemsList(type=card_type, items=[ItemImage(image_id="id")])


class TestImageGallery:
    @pytest.mark.parametrize(
        "card_type",
        ["test", 42, None, CardType.BIG_IMAGE, CardType.ITEMS_LIST],
    )
    def test_wrong_type(self, card_type) -> None:
        items = [ImageGalleryItem(image_id="42:IMAGE_ID")]
        if isinstance(card_type, str):
            with pytest.raises(AliceWrongFieldError):
                ImageGallery(type=card_type, items=items)
        else:
            with pytest.raises(ValidationError):
                ImageGallery(type=card_type, items=items)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.IMAGE_GALLERY, "imagegallery", "IMAGEGALLERY"],
    )
    def test_good_type(self, card_type: str) -> None:
        ImageGallery(
            type=card_type,
            items=[ImageGalleryItem(image_id="42:IMAGE_ID")],
        )
