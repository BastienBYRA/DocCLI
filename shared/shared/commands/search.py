from typing import List
from shared.configs.source_config import SourceConfig
from shared.services.file_service import FileService


class Search():
    file_service: FileService = FileService()
    
    def search(self, config: SourceConfig, search_input: str, exclude_list: List[str]):
        file_service = self.file_service
        searched_path = config.base_dir + self.search_input

        if not file_service.path_exist(searched_path):
            raise ValueError(f"{searched_path} doesn't exist.")
        
        if file_service.is_path_excluded(searched_path, exclude_list):
            raise ValueError(f"The search {search_input} is excluded.")
        
        if file_service.is_folder(searched_path):
            file_service.tree_folder(searched_path, exclude_list)
        else:
            file_service.read_file(searched_path)