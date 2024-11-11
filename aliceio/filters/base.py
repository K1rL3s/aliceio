from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import TYPE_CHECKING, Any, Callable, Union

if TYPE_CHECKING:
    from aliceio.filters.logic import _InvertFilter


class Filter(ABC):  # noqa: B024
    """
    Если вы хотите сделать собственные фильтры, такие же как встроенные фильтры,
    вам нужно будет написать подкласс с переопределением метода :code:`__call__`
    и добавлением атрибутов фильтра.
    """

    if TYPE_CHECKING:
        __call__: Callable[..., Awaitable[Union[bool, dict[str, Any]]]]
    else:  # pragma: no cover

        @abstractmethod
        async def __call__(
            self,
            *args: Any,
            **kwargs: Any,
        ) -> Union[bool, dict[str, Any]]:
            """
            Этот метод надо переопределить.

            Принимает входящее событие и должен возвращать логическое значение или dict.

            :return: :class:`bool` или :class:`dict[str, Any]`
            """

    def __invert__(self) -> "_InvertFilter":
        from aliceio.filters.logic import invert_f

        return invert_f(self)

    def update_handler_flags(self, flags: dict[str, Any]) -> None:  # noqa: B027
        """
        Также, если вы хотите расширить флаги обработчика с помощью этого фильтра,
        вам следует реализовать этот метод

        :param flags: Существующие флаги, могут быть обновлены напрямую.
        """

    def _signature_to_string(self, *args: Any, **kwargs: Any) -> str:
        """
        Подпись к строке.

        :param args:
        :param kwargs:
        """
        items = [repr(arg) for arg in args]
        items.extend([f"{k}={v!r}" for k, v in kwargs.items() if v is not None])

        return f"{type(self).__name__}({', '.join(items)})"

    def __await__(self):  # type: ignore # pragma: no cover # noqa: ANN204
        # Этот метод нужен только для проверки, никогда не вызывается
        return self.__call__
