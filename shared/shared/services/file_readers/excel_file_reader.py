from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from pandas import DataFrame


@dataclass
class ExcelFileReader:

    @staticmethod
    def read(search: Path) -> DataFrame:
        dataframe = pd.read_excel(search)
        return dataframe