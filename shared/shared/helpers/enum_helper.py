from enum import Enum

def value_match_enum(value: str, enum: Enum) -> bool:
    return value in enum.__members__