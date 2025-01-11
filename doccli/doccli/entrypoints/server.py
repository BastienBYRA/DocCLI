from dataclasses import dataclass
from pathlib import Path
from typing import List
from doccli.configs.base_config import BaseConfig
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from doccli.config import ApplicationConfig
from doccli.models.search import Search
from doccli.models.search_result import SearchResult
from doccli.services.file_service import FileService
from doccli.validators.search_validator import SearchValidator
import uvicorn

class EntrypointServer():
    """
    `SERVER` mode starting point.
    
    The application entrypoint to execute the logic specific to the "Server" mode.
    """
    app = FastAPI(title="DocCLI")
    config: BaseConfig = None

    @classmethod
    def run(self) -> None:
        ApplicationConfig.verify_server()
        global config 
        config = ApplicationConfig.get_doccli_config()
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    @app.get("/search/", status_code=status.HTTP_200_OK)
    async def search(search_input: str = "/", exclude_list: str = ""):
        search: Search = SearchValidator.server_side_validator(search_input, exclude_list)
        fullpath: Path = Path(config.base_dir + search_input)

        result: SearchResult
        if FileService.is_folder(fullpath):
            result = FileService.tree_folder(fullpath, config.base_dir)
        else:
            result = FileService.read_file(fullpath)

        return jsonable_encoder(result)

    @app.get("/health/", status_code=status.HTTP_200_OK)
    async def health():
        return {"status": "200"}

# if __name__ == "__main__":
#     setup()
    # uvicorn.run(app)