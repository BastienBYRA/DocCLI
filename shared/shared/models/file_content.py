from dataclasses import dataclass
import json

from pandas import DataFrame


@dataclass
class FileContent:
    filename: str = ""
    content: str | DataFrame = ""

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda self: self.__dict__))