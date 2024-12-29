from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class FileContent:
    filename: str = ""
    content: str | DataFrame = ""