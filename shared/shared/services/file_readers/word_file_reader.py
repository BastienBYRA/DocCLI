from pathlib import Path
from spire.doc import Document

class WordFileReader:
    def read(self, search: Path) -> str:
        doc = Document()
        doc.LoadFromFile(search)
        text = doc.GetText()
        return text