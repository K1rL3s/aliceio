from typing import Union

from .big_image import BigImage
from .image_gallery import ImageGallery
from .items_list import ItemsList

Card = Union[BigImage, ImageGallery, ItemsList]
