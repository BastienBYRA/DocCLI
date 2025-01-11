from dataclasses import dataclass
from pathlib import Path

@dataclass
class DefaultFileReader:

    @staticmethod
    def read(search: Path) -> str:
        text: str = ""
        with search.open() as f:
            for line in f:
                text += f"{line}"
        return text