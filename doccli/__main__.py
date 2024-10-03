from pathlib import Path
from typing import List
from typing_extensions import Annotated
import typer
import command.search as com_search
# from doccli.models.searched_path import Searched_Path

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

    exclude_list: List[str] = exclude.split(",")

    default_dir = r"C:/Users/"
    search_path = Path(default_dir + search_input)
    com_search.is_file_or_dir(search_path, exclude_list)

if __name__ == "__main__":
    app()
