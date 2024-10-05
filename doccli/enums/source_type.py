from enum import Enum
from typing import Optional

from helpers.enum_helper import value_match_enum

class SourceType(Enum):
    OS = "OS"
    GIT = "Git"

def get_source_type(search_source_env: Optional[str]) -> SourceType:
    if not search_source_env:
        raise ValueError("DOCCLI_SOURCE is not defined.")
    
    search_source_upper = search_source_env.upper()
    
    if not value_match_enum(search_source_upper, SourceType):
        raise ValueError("Source specified in DOCCLI_SOURCE is unknown. Expected values: os, git")
        
    return SourceType[search_source_upper]