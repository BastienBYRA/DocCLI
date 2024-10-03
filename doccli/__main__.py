import os
from pathlib import Path
from typing import List
from typing_extensions import Annotated
import typer

from doccli.command.search.search import is_file_or_dir
from doccli.command.search.search_helper import get_search_base_dir, get_search_source, parse_exclude_list


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

    # Get and valid the SEARCH_SOURCE variable
    search_source_env = os.environ.get("SEARCH_SOURCE")
    search_source = get_search_source(search_source_env)
    if search_source is None:
        return None
    
    # Get and valid the SEARCH_BASE_DIR variable
    search_base_dir_env = os.environ.get("SEARCH_BASE_DIR")
    search_base_dir = get_search_base_dir(search_base_dir_env)
    
    # Parse the exclude list
    exclude_list: List[str] = parse_exclude_list(exclude)

    search_path = Path(search_base_dir + search_input)
    is_file_or_dir(search_path, exclude_list)

if __name__ == "__main__":
    app()
