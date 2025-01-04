from dataclasses import dataclass
import json

from pandas import DataFrame


@dataclass
class FileContent:
    filename: str = ""
    content: str | DataFrame = ""

    def to_json(self):
        # https://pythonprinciples.com/ask/how-do-you-json-serialize-a-class-in-python/
        return json.dumps(self, default=lambda self: self.__dict__)