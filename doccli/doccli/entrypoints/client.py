
import os
from typing import List
from typing_extensions import Annotated
from doccli.config import ApplicationConfig
from doccli.commands.CLI.search import CLISearch
from doccli.enums.search_response_type import SearchResponseType
from doccli.models.search import Search
from doccli.models.search_result import SearchResult
from doccli.validators.search_validator import SearchValidator
import typer

class EntrypointClient():
    """
    `CLIENT` mode starting point.

    The application entrypoint to execute the logic specific to the "Client" mode.
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

        ApplicationConfig.verify_client()
        search: Search = SearchValidator.client_side_validator(search_input, exclude)
        result: SearchResult = CLISearch.run(os.getenv("DOCCLI_ENDPOINT"), search_input, exclude)

        while result.response_type == SearchResponseType.DIRECTORY:
            search_input = CLISearch.picker(result, search_input)
            result = CLISearch.run(os.getenv("DOCCLI_ENDPOINT"), search_input, exclude)
                
        result.print_file_content()

    @staticmethod
    @app.command()
    def version() -> None:
        print("0.0.0")

# if __name__ == "__main__":
#     ClientSetup.app()
