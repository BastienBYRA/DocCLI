import os
from typing import Self, cast, override
from pydantic import Field
from shared.configs.base_config import BaseConfig
from shared.enums.source_type import SourceType


class OsConfig(BaseConfig):
    source: SourceType = Field(SourceType.OS, frozen=True)

    @override
    @classmethod
    def create_from_env(cls) -> Self:
        """
        Return a OsConfig object with its values filled from environment variables.
        """
        base_dir = cast(str, os.getenv("DOCCLI_BASE_DIR"))
        return cls(source=SourceType.OS, base_dir=base_dir)