import os
from typing import Self, cast
from pydantic import BaseModel, Field, field_validator

from shared.enums.source_type import SourceType

class BaseConfig(BaseModel):
    """
    BaseConfig serves as the parent class for all configuration models. 
    
    This class is intended to be subclassed and should not be instantiated directly, 
    as it provides a common structure and default settings for derived configuration classes.
    """
    source: SourceType = Field(SourceType.NULL, frozen=True)
    base_dir: str

    @classmethod
    def create_from_env(cls) -> Self:
        """
        Return a BaseConfig object with its values filled from environment variables.
        """
        base_dir = cast(str, os.getenv("DOCCLI_BASE_DIR"))
        return cls(source=SourceType.NULL, base_dir=base_dir)
        

    @field_validator('base_dir')
    def check_base_dir(cls, value: str) -> str:
        if not value:
            raise ValueError("DOCCLI_BASE_DIR is not defined.")
        return value

    @field_validator('source')
    def check_source(cls, value: SourceType) -> SourceType:
        if not value or value is SourceType.NULL:
            raise ValueError("DOCCLI_SOURCE is not defined.")
        return value