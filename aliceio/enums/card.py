from aliceio.enums.base import StrEnum, ValuesEnum


class CardType(StrEnum, ValuesEnum):
    BIG_IMAGE = "BigImage"
    IMAGE_GALLERY = "ImageGallery"
    ITEMS_LIST = "ItemsList"
