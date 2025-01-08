
import os
from typing import List
from CLI.client import CLI
from dotenv import find_dotenv, load_dotenv
from typing_extensions import Annotated
from shared.commands.CLI.search import CLISearch
from shared.config import ApplicationConfig
from shared.configs.base_config import BaseConfig
from shared.enums.execution_mode import ExecutionMode
from shared.enums.search_response_type import SearchResponseType
from shared.models.directory_content import DirectoryContent
from shared.models.search import Search
from shared.models.search_result import SearchResult
from shared.services.file_service import FileService
from shared.validators.search_validator import SearchValidator
import typer

app = typer.Typer()

@app.command()
def search(
    search_input: Annotated[str, typer.Argument()],
    exclude: Annotated[str, typer.Option(prompt_required=False, hidden=True, prompt="A list of regex to exclude files or directories in the form of 'regex1,regex2...'")] = ""
) -> None:
    
    execution_mode: str = ApplicationConfig.get_execution_mode()
    
    # Check if the configuration is valid
    # Should return an error if not
    if execution_mode == ExecutionMode.CLIENT_SERVER:
        ApplicationConfig.verify_client_server()

        config: BaseConfig = ApplicationConfig.get_doccli_config()
        search: Search = SearchValidator.server_side_validator(search_input, exclude)
        
        result: SearchResult
        if FileService.is_folder(search.search_path):
            result = FileService.tree_folder(search, config.base_dir)
        else:
            result = FileService.read_file(search.search_path)

        if result.file_content is None:
            while result.directory_content is not None:
                result = CLI.choose_pick(result, search, config.base_dir)

        result.print_file_content()


    elif execution_mode == ExecutionMode.CLIENT:

        ApplicationConfig.verify_client()
        search: Search = SearchValidator.client_side_validator(search_input, exclude)
        result: SearchResult = CLISearch.run(os.getenv("DOCCLI_ENDPOINT"), search_input, exclude)

        # if result.response_type is not SearchResponseType.FILE:
            # while result.response_type is SearchResponseType.DIRECTORY:
            #     result = CLI.choose_pick(result, search, config.base_dir)

        while result.response_type is SearchResponseType.DIRECTORY:
            new_search_result: str = CLI.choose_pick_cli(result, search_input)
            result = CLISearch.run(os.getenv("DOCCLI_ENDPOINT"), new_search_result, exclude)
                
        result.print_file_content()

        # if result.file_content is None:
        #     while result.directory_content is not None:
        #         result = CLI.choose_pick(result, search, config.base_dir)

        # result.print_file_content()
        
    else:
        raise ValueError("Running as a mode is isn't supposed to.")
    
    

    

    # result: DirectoryContent | FileContent = Entrypoint.search(search_input, exclude)

    # while isinstance(result, DirectoryContent):
    #     result = CLI.choose_pick(result)

    # if isinstance(result, FileContent):
    #     print("-------------- START CONTENT --------------")
    #     print(result.content)
    #     print("--------------- END CONTENT ---------------")
    
    exit(0)
    
@app.command()
def version():
    print("DocCLI: Version 0.1.0")
    print("Project: https://github.com/BastienBYRA/DocCLI")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), verbose=True)
    app()
