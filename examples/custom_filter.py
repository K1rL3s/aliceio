from typing import Any, List

from aliceio import Router
from aliceio.filters import BaseFilter
from aliceio.types import Message

router = Router()


class InWordsFilter(BaseFilter):
    def __init__(self, words: List[str]) -> None:
        self.words = words

    async def __call__(self, message: Message) -> bool:
        return message.command.lower() in self.words


@router.message(InWordsFilter(["да", "ок", "хорошо"]))
async def yes_handler(message: Message) -> Any:
    ...
