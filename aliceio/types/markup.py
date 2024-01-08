from aliceio.types.base import AliceObject


class Markup(AliceObject):
    """
    Формальные характеристики реплики, которые удалось выделить Яндекс Диалогам.
    Объект отсутствует, если ни одно из вложенных свойств не применимо.

    https://yandex.ru/dev/dialogs/alice/doc/request-simpleutterance.html#request-simpleutterance__markup-desc
    """  # noqa

    dangerous_context: bool
