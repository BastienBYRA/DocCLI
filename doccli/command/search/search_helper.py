# doccli/command/search_helper.py

from doccli.enum.search_source import Search_Source
from doccli.helper.enum_helper import value_match_enum
from typing import List

def get_search_source(search_source_env: str) -> Search_Source:
    if not search_source_env:
        print("SEARCH_SOURCE is not defined.")
        return None

    search_source_upper = search_source_env.upper()
    
    if value_match_enum(search_source_upper, Search_Source):
        return Search_Source[search_source_upper]
    
    print("Source specified in SEARCH_SOURCE is unknown. Expected values: os, git")
    return None


def get_search_base_dir(search_base_dir_env: str) -> str:
    if not search_base_dir_env:
        print("SEARCH_BASE_DIR is not defined.")
        return None
    return search_base_dir_env


def parse_exclude_list(exclude: str) -> List[str]:
    return exclude.split(",") if exclude else []
