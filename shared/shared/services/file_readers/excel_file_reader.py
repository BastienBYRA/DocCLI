from pathlib import Path
import pandas as pd

class ExcelFileReader:
    def read(self, search: Path) -> str:
        dataframe = pd.read_excel(search)
        return dataframe