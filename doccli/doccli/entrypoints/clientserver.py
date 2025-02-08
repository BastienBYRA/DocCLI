import os
from pathlib import Path
from typing import List
from typing_extensions import Annotated
from doccli.config import ApplicationConfig
from doccli.commands.CLI.search import CLISearch
from doccli.configs.base_config import BaseConfig
from doccli.services.file_service import FileService
from doccli.enums.search_response_type import SearchResponseType
from doccli.models.search import Search
from doccli.models.search_result import SearchResult
from doccli.validators.search_validator import SearchValidator
import typer

class EntrypointClientServer():
    """
    `CLIENT-SERVER` mode starting point.

    The application entrypoint to execute the logic specific to the "Client-Server" mode.
    """

    app = typer.Typer()

    @classmethod
    def run(cls) -> None:
        cls.app()

    @staticmethod
    @app.command()
    def search(search_input: Annotated[str, typer.Argument()]) -> None:

        # Argument to implement later
        exclude = ""

        ApplicationConfig.verify_client_server()

        config: BaseConfig = ApplicationConfig.get_doccli_config()
        search: Search = SearchValidator.server_side_validator(search_input, exclude)
        fullpath: Path = Path(config.base_dir + search_input)
        
        result: SearchResult
        if FileService.is_folder(fullpath):
            result = FileService.tree_folder(fullpath, config.base_dir)
        else:
            result = FileService.read_file(fullpath)

        while result.response_type == SearchResponseType.DIRECTORY:
            search_input = CLISearch.picker(result, search_input)
            fullpath = Path(config.base_dir + search_input)

            if FileService.is_folder(fullpath):
                result = FileService.tree_folder(fullpath, config.base_dir)
            else:
                result = FileService.read_file(fullpath)

        result.print_file_content()

    @staticmethod
    @app.command()
    def version() -> None:
        print("DocCLI; https://github.com/BastienBYRA/DocCLI")
        print("0.1.0")

# if __name__ == "__main__":
#     ClientSetup.app()
