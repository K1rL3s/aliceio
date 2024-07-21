from abc import ABC

from aliceio.handlers.base import BaseHandler
from aliceio.types import AccountLinkingComplete


# TODO: узнать, передаётся ли поле request (и с чем) при подтверждении авторизации
class AccountLinkingCompleteHandler(BaseHandler[AccountLinkingComplete], ABC):
    """Базовый класс для обработчиков успешной авторизации пользоватя."""
