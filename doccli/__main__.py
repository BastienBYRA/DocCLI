from pathlib import Path
import typer
import command.search as com_search

app = typer.Typer()

@app.command()
def main():
    print("Hello from doccli")

@app.command()
def search(search_input: str) -> None:
    default_dir = r"C:/Users/Bastien"
    search_path = Path(default_dir + search_input)
    com_search.is_file_or_dir(search_path)


if __name__ == "__main__":
    app()
