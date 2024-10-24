import os

from pydantic import BaseModel
from shared.shared.configs.source_config import SourceConfig
from shared.shared.enums.source_type import SourceType, get_source_type
from shared.shared.helpers.envvar_helper import get_git_env, get_os_env
from shared.shared.models.search_command import SearchCommand
from shared.shared.services.file_service import FileService
from shared.shared.services.git_service import GitService


class Entrypoint():

    def search(self, search_input: str, exclude: str):

        # Get and valid the SEARCH_SOURCE variable
        doccli_source = get_source_type(os.getenv("DOCCLI_SOURCE"))
        if not doccli_source:
            raise ValueError("DOCCLI_SOURCE is not defined.")
        
        # Get the config depending of the source the used specified
        config: SourceConfig
        match SourceType(doccli_source):
            case SourceType.OS:
                config = get_os_env()
            case SourceType.GIT:
                config = get_git_env()
                GitService.clone_repo()
            case _:
                raise ValueError("The source specified is unknown. Expected values: os, git")

        # Create a SearchCommand object with necessary values to the "search" command
        # search_info = SearchCommand(config, self.search_input, self.exclude)

        file_service: FileService = FileService()

        # searched_filepath: str = config.base_dir + search_input

        if not file_service.path_exist(searched_filepath):
            raise ValueError(f"{searched_filepath} doesn't exist.")
        
        if file_service.is_folder(searched_filepath):
            file_service.tree_folder(searched_filepath)
        else:
            file_service.read_file(searched_filepath)

