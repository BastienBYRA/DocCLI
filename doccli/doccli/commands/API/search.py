from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder

from doccli.config import ApplicationConfig
from doccli.services.file_service import FileService
from doccli.models.search_result import SearchResult
from doccli.models.search import Search
from doccli.validators.search_validator import SearchValidator


load_dotenv(find_dotenv(), verbose=True)
app = FastAPI()

ApplicationConfig.verify_server()
config = ApplicationConfig.get_doccli_config()

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