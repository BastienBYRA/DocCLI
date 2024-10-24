from pathlib import Path


class DefaultFileReader:
    def read(self, search: Path) -> str:
        text: str = ""
        with search.open() as f:
            for line in f:
                text += f"{line} \n"
        return text