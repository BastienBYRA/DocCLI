from typing import Optional


class SourceConfig:
    def __init__(self, source: Optional[str] = None, base_dir: Optional[str]  = None) -> None:
        if not source:
            raise ValueError("DOCCLI_SOURCE is not defined.")
        
        print(base_dir)
        if not base_dir:
            raise ValueError("DOCCLI_BASE_DIR is not defined.")
        
        self.source = source
        self.base_dir = base_dir