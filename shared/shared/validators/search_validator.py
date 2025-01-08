import os
from pathlib import Path
import re
from typing import List

from fastapi import HTTPException

from loguru import logger
from shared.models.search import Search

class SearchValidator:
    """
    Validates the specific components and arguments required for the "search" command.
    """

    ##############################################
    #### CLIENT SIDE VALIDATION SPECIFIC
    ##############################################
    
    @staticmethod
    def client_side_validator(user_search_input: str, exclusion_list: str) -> Search:
        """
        Validates the user-provided search input and exclusion list for client-side validation.

        This function performs the following checks:
        1. Ensures the search path is not empty. If empty, defaults to "/".
        2. Validates that the search path adheres to the allowed regex pattern: ^[a-zA-Z0-9_\-./\\]+$.
        3. Checks if the exclusion list is empty and handles it as None.
        4. Ensures that all regex patterns in the exclusion list are valid and do not exclude the search path.

        :param user_search_input: The path provided by the user for the search operation.
        :param exclusion_list: A comma-separated string of regex patterns to exclude certain paths.
        :return: A Search object initialized with the validated path and processed exclusion list.
        :raises ValueError: If the search path is invalid or any regex in the exclusion list excludes the search path.
        """

        # Check everything is OK with the Path provided
        is_path_empty: bool = SearchValidator.path_is_empty(user_search_input)
        if is_path_empty is True:
            user_search_input = "/"
        
        is_path_valid: bool = SearchValidator.path_respect_regex_condition(user_search_input)
        if is_path_valid is False:
            raise ValueError("The path provided is not valid, the Path must respect the following regex : ^[a-zA-Z0-9_\-./\\]+$")
        
        # Check everything is OK with the exclusion list provided
        is_exclusion_list_empty: bool = SearchValidator.exclusion_list_is_empty(exclusion_list)
        if is_exclusion_list_empty is True:
            exclusion_list = None

        is_exclusion_list_valid: bool = SearchValidator.exclusion_list_is_valid(user_search_input, exclusion_list)
        if is_exclusion_list_valid is False:
            raise ValueError('There is a problem with one of the regex provided in the "--exclusion_list" arguments')

        return Search(Path(user_search_input), exclusion_list.split(","))
    

    def path_is_empty(user_search_input: str) -> bool:
        """
        Checks if the user-provided search path is empty.

        :param user_search_input: The path provided by the user.
        :return: True if the path is empty, False otherwise.
        """
        if not user_search_input:
            logger.warning("No path provided for the search, defaulted to '/'")
            return True
        return False


    def path_respect_regex_condition(user_search_input: str) -> bool:
        """
        Validates that the user-provided search path adheres to the allowed regex pattern.

        The allowed regex pattern is: ^[a-zA-Z0-9_\-./\\]+$

        :param user_search_input: The path provided by the user.
        :return: True if the path matches the allowed regex pattern, False otherwise.
        """
        allowed_pattern = r"^[a-zA-Z0-9_\-./\\]+$"
        if not re.match(allowed_pattern, user_search_input):
            return False
        return True


    def exclusion_list_is_empty(exclusion_list: str) -> bool:
        """
        Checks if the user-provided exclusion list is empty.

        :param exclusion_list: A comma-separated string of regex patterns.
        :return: True if the exclusion list is empty, False otherwise.
        """
        if not exclusion_list:
            return True
        return False


    def exclusion_list_is_valid(user_search_input: str, exclusion_list: str) -> bool:
        """
        Validates the exclusion list against the user-provided search path.

        This function performs the following checks:
        1. Verifies that no regex in the exclusion list matches the search path.
        2. Ensures that all regex patterns in the exclusion list are valid.

        :param user_search_input: The path provided by the user.
        :param exclusion_list: A comma-separated string of regex patterns.
        :return: True if the exclusion list is valid, False otherwise.
        :raises ValueError: If a regex in the exclusion list excludes the search path or if the regex is invalid.
        """
        if not exclusion_list:
            return True

        exclude_list: List[str] = exclusion_list.split(",")

        try:
            if len(exclude_list) > 0:
                for reg in exclude_list:
                    if re.search(reg, user_search_input) is not None:
                        raise ValueError(f"The following regex {reg} excludes your search.")
        except Exception as e:
            raise ValueError(f'There is a problem with one of the regex provided in the "--exclusion_list" arguments; {e}')

        return True  

    ##############################################
    #### SERVER SIDE VALIDATION
    ##############################################

    @staticmethod
    def server_side_validator(user_search_input: str, exclusion_list: str) -> bool:
        """
        Validates the user-provided search input and exclusion list for server-side validation.

        This function performs the following checks:
        1. Calls the `client_side_validator` to ensure the input passes client-side validation.
        2. Ensures that the resolved full path exists on the server.
        3. Verifies that the resolved path is within the base directory to prevent directory traversal attacks.

        :param user_search_input: The path provided by the user for the search operation.
        :param exclusion_list: A comma-separated string of regex patterns to exclude certain paths.
        :return: True if all validations pass.
        :raises HTTPException: If any of the validations fail, with a corresponding error code and message.
        """
        base_dir: str = os.getenv("DOCCLI_BASE_DIR")

        try:
            SearchValidator.client_side_validator(user_search_input, exclusion_list)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"The Client-side validator failed; {e}")
        
        base_dir_path: Path = Path(base_dir)
        user_fullpath: Path = Path(base_dir + user_search_input)

        path_exist: bool = SearchValidator.path_exists(user_fullpath)
        if path_exist is False:
            raise HTTPException(status_code=404, detail="The path provided doesn't exist")
        
        path_is_valid: bool = SearchValidator.path_is_valid(base_dir_path, user_fullpath)
        if path_is_valid is False:
            raise HTTPException(status_code=404, detail=f"The search path {user_search_input} is outside the base directory configured by the administrator.")

        return True


    def path_exists(user_search_path: Path) -> bool:
        """
        Checks if the resolved user search path exists on the server.

        :param user_search_path: The resolved path provided by the user.
        :return: True if the path exists, False otherwise.
        """
        return user_search_path.exists()


    def path_is_valid(base_dir: Path, user_search_path: Path) -> bool:
        """
        Validates that the resolved user search path is within the base directory.

        This function ensures the following:
        1. Prevents directory traversal attacks by verifying that the user search path
        is within the base directory configured by the administrator.

        :param base_dir: The base directory configured for the application.
        :param user_search_path: The resolved path provided by the user.
        :return: True if the path is within the base directory, False otherwise
        """
        # Prevent user from doing a Directory traversal attack
        if str(base_dir.resolve()) not in str(user_search_path.resolve()):
            return False
        return True
