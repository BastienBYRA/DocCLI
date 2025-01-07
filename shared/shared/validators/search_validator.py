import os
from pathlib import Path
import re
from typing import List

from loguru import logger
from shared.models.search import Search

class SearchValidator:
    """
    Validates the specific components and arguments required for the "search" command.
    """
        
    @staticmethod
    def validate(user_search_input: str, exclude: str) -> Search:
        search_path: Path = None
        exclude_list: List[str] = []
        base_dir: str = os.getenv("DOCCLI_BASE_DIR")

        # Check the user input
        if not user_search_input:
            logger.warning("No path provided for the search, defaulted to \"/")
            user_search_input = "/"
        
        SearchValidator.validate_search_path_input(user_search_input)
        search_path: Path = Path(base_dir + user_search_input)

        # Check the exclude list
        if exclude:
            exclude_list = SearchValidator.validate_exclude_list_input(search_path, exclude)

        return Search(search_path, exclude_list)
    

    def validate_search_path_input(user_search_input: str) -> Path:
        # Check the user_input is defined
        if not user_search_input:
            raise ValueError("The search is empty")
        

        doccli_base_dir: Path = Path(os.getenv("DOCCLI_BASE_DIR"))
        user_search_path: Path = Path(str(doccli_base_dir) + user_search_input)

        # Check the Path is valid
        user_search_input_valid = user_search_path.exists()
        if user_search_input_valid is False:
            raise ValueError(f"{user_search_input} doesn't exist.")
        
        # Prevent user from doing a Directory traversal attack
        if str(doccli_base_dir.resolve()) not in str(user_search_path.resolve()):
            raise ValueError(f"The search path {user_search_path.resolve()} is outside the base directory configured by the administrator.")
        
        return Path(str(doccli_base_dir) + user_search_input)


    def validate_exclude_list_input(search: Path, exclude: str) -> List[str]:
        if not exclude:
            return []
        
        exclude_list: List[str] = exclude.split(",")
        
        if len(exclude_list) > 0:
            for reg in exclude_list:
                if re.search(reg, str(search)) is not None:
                    raise ValueError(f"The following regex {reg} exclude your search")
        
        return exclude.split(",")


