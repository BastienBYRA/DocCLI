from dotenv import find_dotenv, load_dotenv
from typing_extensions import Annotated
import typer
from shared.entrypoint import Entrypoint

app = typer.Typer()

@app.command()
def search(
    search_input: Annotated[str, typer.Argument()],
    exclude: Annotated[str, typer.Option(prompt_required=False, hidden=True, prompt="A list of regex to exclude files or directories in the form of 'regex1,regex2...'")] = ""
) -> None:
    Entrypoint.search(search_input, exclude)
    
@app.command()
def version():
    print("DocCLI: Version 0.1.0")
    print("Project: https://github.com/BastienBYRA/DocCLI")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), verbose=True)
    app()
