import os
from dotenv import load_dotenv
from typing_extensions import Annotated
import typer

from command.search.search import search_entrypoint_source
from enums.source_type import SourceType, get_source_type
from helpers.envvar_helper import get_git_env, get_os_env
from models.search_command import SearchCommand
from models.source_config import SourceConfig

app = typer.Typer()

@app.command()
def main():
    print("Hello from doccli")

@app.command()
def search(
           search_input: Annotated[
               str, typer.Argument(envvar="SEARCH_INPUT")],
           exclude: Annotated[
               str, typer.Option(prompt_required=False ,hidden=True, prompt="A list of regex to exclude files or directories in the form of 'regex1,regex2...'")] = "") -> None:

    load_dotenv()

    # Get and valid the SEARCH_SOURCE variable
    doccli_source = get_source_type(os.getenv("DOCCLI_SOURCE"))
    if not doccli_source:
        raise ValueError("DOCCLI_SOURCE is not defined.")
    
    # Get the config depending of the source the used specified
    source: SourceConfig
    match SourceType(doccli_source):
        case SourceType.OS:
            source = get_os_env()
        case SourceType.GIT:
            source = get_git_env()
        case _:
            print("Shouldn't be here")

    print(source.base_dir)
    # Create a SearchCommand object with necessary values to the "search" command
    search_info = SearchCommand(source, search_input, exclude)
    search_entrypoint_source(search_info)

if __name__ == "__main__":
    app()
