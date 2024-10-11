from pathlib import Path
from typing import List

from models.source_config import SourceConfig

class SearchCommand:
    def __init__(self, source_config: SourceConfig, search_path: str, exclude: str):
        self.source_config = source_config

        if not search_path:
            raise ValueError("Search path not found.")
        self.search_path = Path(search_path)

        self.exclude: List[str] = exclude.split(",") if exclude else []

    