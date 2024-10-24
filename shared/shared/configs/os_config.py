from models.source_config import SourceConfig


class OsConfig(SourceConfig):
    def __init__(self, base_dir) -> None:
        super().__init__(source="os", base_dir=base_dir)