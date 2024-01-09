from enum import Enum
from typing import List


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> List[str]:
        return [e.value for e in cls]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)
