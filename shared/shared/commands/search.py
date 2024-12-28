from dataclasses import dataclass
from pathlib import Path
from typing import List
from shared.configs.base_config import BaseConfig
from shared.services.file_service import FileService

@dataclass
class Search():
    file_service: FileService = FileService()
    
    def search(self, config: BaseConfig, search_input: str, exclude_list: List[str]) -> None:
        file_service: FileService = self.file_service
        searched_path = Path(config.base_dir + search_input)

        if not file_service.path_exist(searched_path):
            raise ValueError(f"{searched_path} doesn't exist.")
        
        if file_service.is_path_excluded(searched_path, exclude_list):
            raise ValueError(f"The search {search_input} is excluded.")

        if file_service.is_folder(searched_path):
            file_service.tree_folder(searched_path, exclude_list, config)
        else:
            file_service.read_file(searched_path)