from enum import Enum
from typing import Type

def value_match_enum(value: str, enum: Type[Enum]) -> bool:
    return value in enum.__members__