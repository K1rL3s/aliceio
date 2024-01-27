import datetime
import json
from enum import Enum
from typing import Any, Callable, Dict, Protocol

from aiohttp import JsonPayload

from aliceio.dispatcher.event.bases import REJECTED, UNHANDLED
from aliceio.types import InputFile


class PrepareValue(Protocol):  # pragma: no cover
    def __call__(self, value: Any, files: Dict[str, Any]) -> Any:
        ...


# Ключи, у которых значение = None, не пропускаются, потому что иначе не получится
# установить None в значение хранилища состояний API Алисы
def prepare_value(value: Any, files: Dict[str, Any]) -> Any:
    """Подготовка значения перед отправкой."""
    if value in (None, UNHANDLED, REJECTED):
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, InputFile):
        key = "file"
        files[key] = value
        return f"attach://{key}"
    if isinstance(value, dict):
        return {key: prepare_value(item, files=files) for key, item in value.items()}
    if isinstance(value, list):
        return [prepare_value(item, files=files) for item in value]
    if isinstance(value, datetime.timedelta):
        now = datetime.datetime.now()
        return str(round((now + value).timestamp()))
    if isinstance(value, datetime.datetime):
        return str(round(value.timestamp()))
    if isinstance(value, Enum):
        return prepare_value(value.value, files=files)
    return value


def build_json_payload(
    value: Any,
    prepare_value_fn: PrepareValue = prepare_value,
    json_dumps: Callable[..., str] = json.dumps,
) -> JsonPayload:
    return JsonPayload(
        value=prepare_value_fn(value=value, files={}),
        dumps=json_dumps,
    )
