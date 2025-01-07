from typing import List
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from shared.config import ApplicationConfig
from shared.models.search import Search
from shared.models.search_result import SearchResult
from shared.services.file_service import FileService
from shared.validators.search_validator import SearchValidator

load_dotenv(find_dotenv(), verbose=True)
app = FastAPI()

ApplicationConfig.verify_server()
config = ApplicationConfig.get_doccli_config()

@app.get("/search/", status_code=status.HTTP_200_OK)
async def search(search_input: str = "/", exclude_list: str = ""):
    search: Search = SearchValidator.validate(search_input, exclude_list)
        
    result: SearchResult
    if FileService.is_folder(search.search_path):
        result = FileService.tree_folder(search, config.base_dir)
    else:
        result = FileService.read_file(search.search_path)

    return jsonable_encoder(result)

@app.get("/health/", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "200"}

# if __name__ == "__main__":
#     setup()
    # uvicorn.run(app)