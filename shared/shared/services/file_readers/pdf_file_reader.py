from pathlib import Path
from pypdf import PdfReader



class PdfFileReader:
    def read(self, search: Path) -> str:
        reader = PdfReader("example.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text