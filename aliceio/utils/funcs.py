import datetime
import json
from enum import Enum
from typing import Any, Callable, Literal, Protocol, Union

from aiohttp import JsonPayload

from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.types import InputFile
from aliceio.types.base import AliceObject


class PrepareValue(Protocol):  # pragma: no cover
    def __call__(
        self,
        value: Any,
        files: dict[str, Any],
        _dumps_json: Union[Callable[..., str], Literal[False]] = False,
    ) -> Any: ...


# Ключи, у которых значение = None, не пропускаются, потому что иначе не получится
# установить None в значение хранилища состояний API Алисы
def prepare_value(
    value: Any,
    files: dict[str, Any],
    _dumps_json: Union[Callable[..., str], Literal[False]] = False,
) -> Any:
    """Подготовка значения перед отправкой."""
    if value in (None, UNHANDLED, REJECTED):
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, InputFile):
        key = "file"  # aiogram: key = secrets.token_urlsafe(10)
        files[key] = value
        return f"attach://{key}"
    if isinstance(value, dict):
        value = {key: prepare_value(item, files=files) for key, item in value.items()}
        if _dumps_json:
            return _dumps_json(value)
        return value
    if isinstance(value, list):
        value = [prepare_value(item, files=files) for item in value]
        if _dumps_json:
            return _dumps_json(value)
        return value
    if isinstance(value, datetime.timedelta):
        now = datetime.datetime.now()
        return str(round((now + value).timestamp()))
    if isinstance(value, datetime.datetime):
        return str(round(value.timestamp()))
    if isinstance(value, Enum):
        return prepare_value(value.value, files=files)
    if isinstance(value, AliceObject):
        return prepare_value(
            value.model_dump(warnings=False),
            files=files,
            _dumps_json=_dumps_json,
        )
    if _dumps_json:
        return _dumps_json(value)
    return value


# TODO: В prepavre_value_fn не передаётся json_dumps, пофиксить?
def build_json_payload(
    value: Any,
    prepare_value_fn: PrepareValue = prepare_value,
    json_dumps: Callable[..., str] = json.dumps,
) -> JsonPayload:
    return JsonPayload(
        value=prepare_value_fn(
            value=value,
            files={},
        ),
        dumps=json_dumps,
    )
