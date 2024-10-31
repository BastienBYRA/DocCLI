from enum import StrEnum
from typing import Optional

from shared.helpers.enum_helper import value_match_enum

class SourceType(StrEnum):
    OS = "os"
    GIT = "git"
    NULL = "null"

def get_source_type(search_source_env: Optional[str]) -> SourceType:
    if not search_source_env:
        raise ValueError("DOCCLI_SOURCE is not defined.")
    
    search_source_upper = search_source_env.upper()
    
    if not value_match_enum(search_source_upper, SourceType):
        raise ValueError("Source specified in DOCCLI_SOURCE is unknown. Expected values: os, git")
        
    return SourceType[search_source_upper]