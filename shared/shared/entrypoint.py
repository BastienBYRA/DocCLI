from dataclasses import dataclass
import os
from typing import List

from shared.commands.search import Search
from shared.configs.git_config import GitConfig
from shared.configs.base_config import BaseConfig
from shared.configs.os_config import OsConfig
from shared.enums.source_type import SourceType, get_source_type
from shared.services.git_service import GitService

@dataclass
class Entrypoint():

    @staticmethod
    def search(search_input: str, exclude: str) -> None:

        # Get and valid the SEARCH_SOURCE variable
        doccli_source = get_source_type(os.getenv("DOCCLI_SOURCE"))
        if not doccli_source:
            raise ValueError("DOCCLI_SOURCE is not defined.")
        
        # Get the config depending of the source the used specified
        config: BaseConfig
        match SourceType(doccli_source):
            case SourceType.OS:
                config = OsConfig.create_from_env()
            case SourceType.GIT:
                config = GitConfig.create_from_env()
                GitService(git_config=config).clone_repo()
            case _:
                raise ValueError("The source specified is unknown. Expected values: os, git")
            
        # Convert the exclude list given by the user to a real list
        exclude_list: List[str]
        if exclude:
            exclude_list = exclude.split(",")
        else:
            exclude_list = []
        
        return Search().search(config, search_input, exclude_list)