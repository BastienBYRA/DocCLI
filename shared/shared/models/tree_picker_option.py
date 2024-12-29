from dataclasses import dataclass


@dataclass
class TreePickerOption:
    index: int = -1
    name: str = ""