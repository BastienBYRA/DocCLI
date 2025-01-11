
from typing import List
from typing_extensions import Annotated
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
        print(search_input)

    @staticmethod
    @app.command()
    def version() -> None:
        print("0.0.0")

# if __name__ == "__main__":
#     ClientSetup.app()
