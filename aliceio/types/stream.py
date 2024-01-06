from aliceio.types import AliceObject


class Stream(AliceObject):
    """
    Описание аудиопотока.

    https://yandex.ru/dev/dialogs/alice/doc/response-audio-player.html#direct-play__audio-player-item-stream-desc
    """  # noqa

    url: str
    offset_ms: int
    token: str
