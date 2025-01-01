from dataclasses import dataclass


@dataclass
class DirectoryContentOption:
    index: int = -1
    name: str = ""