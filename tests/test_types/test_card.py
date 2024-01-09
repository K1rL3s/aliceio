import pytest

from aliceio.enums.card import CardType
from aliceio.types import BigImage, Card, ImageGallery, ImageGalleryItem, ItemsList


class TestBigImage:
    @pytest.mark.parametrize(
        "card_type",
        ["test", CardType.ITEMS_LIST, CardType.IMAGE_GALLERY],
    )
    def test_wrong_type(self, card_type: str) -> None:
        with pytest.raises(ValueError):
            BigImage(type=card_type)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.BIG_IMAGE, "bigimage", "BIGIMAGE"],
    )
    def test_good_type(self, card_type: str) -> None:
        BigImage(type=card_type)


class TestItemsList:
    @pytest.mark.parametrize(
        "card_type",
        ["test", 42, None, CardType.BIG_IMAGE, CardType.IMAGE_GALLERY],
    )
    def test_wrong_type(self, card_type: str) -> None:
        with pytest.raises(ValueError):
            ItemsList(type=card_type)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.ITEMS_LIST, "itemslist", "ITEMSLIST"],
    )
    def test_good_type(self, card_type: str) -> None:
        ItemsList(type=card_type)


class TestImageGallery:
    @pytest.mark.parametrize(
        "card_type",
        ["test", 42, None, CardType.BIG_IMAGE, CardType.ITEMS_LIST],
    )
    def test_wrong_type(self, card_type: str) -> None:
        with pytest.raises(ValueError):
            ImageGallery(
                type=card_type,
                items=[ImageGalleryItem(image_id="42:IMAGE_ID")],
            )

    @pytest.mark.parametrize(
        "card_type",
        [CardType.IMAGE_GALLERY, "imagegallery", "IMAGEGALLERY"],
    )
    def test_good_type(self, card_type: str) -> None:
        ImageGallery(
            type=card_type,
            items=[ImageGalleryItem(image_id="42:IMAGE_ID")],
        )


class TestCard:
    @pytest.mark.parametrize(
        "card_type",
        [
            "42",
            "random",
            "any",
            "bigimage",
            "BIGIMAGE",
            "itemslist",
            "ITEMSLIST",
            "imagegallery",
            "IMAGEGALLERY",
        ],
    )
    def test_wrong_type(self, card_type: str) -> None:
        class AnyCard(Card):
            pass

        with pytest.raises(ValueError):
            AnyCard(type=card_type)

    @pytest.mark.parametrize(
        "card_type",
        [CardType.BIG_IMAGE, CardType.ITEMS_LIST, CardType.IMAGE_GALLERY],
    )
    def test_good_type(self, card_type: str) -> None:
        class AnyCard(Card):
            pass

        AnyCard(type=card_type)
