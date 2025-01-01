from dataclasses import dataclass
import json

from pandas import DataFrame


@dataclass
class FileContent:
    filename: str = ""
    content: str | DataFrame = ""

    def to_json(self):
        return json.dumps(self.__dict__) 