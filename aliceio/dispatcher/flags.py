from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, Union, cast, overload

from magic_filter import AttrDict, MagicFilter

if TYPE_CHECKING:
    from aliceio.dispatcher.event.handler import HandlerObject


@dataclass(frozen=True)
class Flag:
    name: str
    value: Any


@dataclass(frozen=True)
class FlagDecorator:
    flag: Flag

    @classmethod
    def _with_flag(cls, flag: Flag) -> "FlagDecorator":
        return cls(flag)

    def _with_value(self, value: Any) -> "FlagDecorator":
        new_flag = Flag(self.flag.name, value)
        return self._with_flag(new_flag)

    @overload
    def __call__(self, value: Callable[..., Any], /) -> Callable[..., Any]:  # type: ignore
        pass

    @overload
    def __call__(self, value: Any, /) -> "FlagDecorator":
        pass

    @overload
    def __call__(self, **kwargs: Any) -> "FlagDecorator":
        pass

    def __call__(
        self,
        value: Optional[Any] = None,
        **kwargs: Any,
    ) -> Union[Callable[..., Any], "FlagDecorator"]:
        if value and kwargs:
            raise ValueError(
                "The arguments `value` and **kwargs can not be used together",
            )

        if value is not None and callable(value):
            value.aliceio_flag = {
                **extract_flags_from_object(value),
                self.flag.name: self.flag.value,
            }
            return cast(Callable[..., Any], value)
        return self._with_value(AttrDict(kwargs) if value is None else value)


if TYPE_CHECKING:

    class _ChatActionFlagProtocol(FlagDecorator):
        def __call__(  # type: ignore[override]
            self,
            action: str = ...,
            interval: float = ...,
            initial_sleep: float = ...,
            **kwargs: Any,
        ) -> FlagDecorator:
            pass


class FlagGenerator:
    def __getattr__(self, name: str) -> FlagDecorator:
        if name[0] == "_":
            raise AttributeError("Flag name must NOT start with underscore")
        return FlagDecorator(Flag(name, True))

    if TYPE_CHECKING:
        chat_action: _ChatActionFlagProtocol


def extract_flags_from_object(obj: Any) -> dict[str, Any]:
    if not hasattr(obj, "aliceio_flag"):
        return {}
    return cast(dict[str, Any], obj.aliceio_flag)


def extract_flags(handler: Union["HandlerObject", dict[str, Any]]) -> dict[str, Any]:
    """
    Извлекает флаги из контекстных данных обработчика или мидлваря.

    :param handler: Объект обработчика или данные.
    :return: Словарь со всеми флагами обработчика.
    """
    if isinstance(handler, dict) and "handler" in handler:
        handler = handler["handler"]
    if hasattr(handler, "flags"):
        return handler.flags
    return {}


def get_flag(
    handler: Union["HandlerObject", dict[str, Any]],
    name: str,
    *,
    default: Optional[Any] = None,
) -> Any:
    """
    Получить флаг по имени (ключу).

    :param handler: Объект обработчика или данные.
    :param name: Имя флага.
    :param default: Значение по умолчанию (None).
    :return: Значение флага или default.
    """
    flags = extract_flags(handler)
    return flags.get(name, default)


def check_flags(
    handler: Union["HandlerObject", dict[str, Any]],
    magic: MagicFilter,
) -> Any:
    """
    Проверка флагов с помощью magic filter'а.

    :param handler: Объект обработчика или данные.
    :param magic: Экземпляр magic filter'а.
    :return: Результат проверки magic filter'а.
    """
    flags = extract_flags(handler)
    return magic.resolve(AttrDict(flags))
