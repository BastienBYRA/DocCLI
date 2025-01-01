from enum import Enum
from typing import Type

def value_in_enum(value: str, enum: Type[Enum]) -> bool:
    if value in enum:
        return value