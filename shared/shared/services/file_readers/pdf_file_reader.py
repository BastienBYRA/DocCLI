from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader


@dataclass
class PdfFileReader:

    @staticmethod
    def read(search: Path) -> str:
        reader = PdfReader(search)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text