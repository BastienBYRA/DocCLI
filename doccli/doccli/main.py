import os
from dotenv import find_dotenv, load_dotenv

from doccli.config import ApplicationConfig
from doccli.enums.execution_mode import ExecutionMode
from doccli.entrypoints.client import EntrypointClient
from doccli.entrypoints.server import EntrypointServer

def start_app() -> None:
    execution_mode: str = ApplicationConfig.get_execution_mode()

    if execution_mode == ExecutionMode.CLIENT_SERVER:
        exit(1)
    elif execution_mode == ExecutionMode.CLIENT:
        EntrypointClient.run()
    elif execution_mode == ExecutionMode.SERVER:
        EntrypointServer.run()
    else:
        raise ValueError("The DOCCLI_MODE values is not recognized.")

    exit(0)

if __name__ == "__main__":
    load_dotenv(find_dotenv(), verbose=True)
    print(os.getenv("DOCCLI_MODE"))
    print("HEY")
    start_app()