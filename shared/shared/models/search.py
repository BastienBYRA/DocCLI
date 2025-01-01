from dataclasses import dataclass
from pathlib import Path
from typing import List
# import os
# from loguru import logger
# from pydantic import BaseModel, field_validator, ValidationError

@dataclass
class Search():
    search_path: Path
    exclude_list: List[str]

    # @field_validator('user_search_input', mode="after")
    # def search_path_defined(cls, value: str) -> str:
    #     """
    #     Ensure the input is provided, if not, set default to "/"
    #     """
    #     if not value:
    #         logger.warning("No path provided for the search, defaulted to \"/\"")
    #         return "/"  # Default value if not provided
    #     return value

    # @field_validator('user_search_input', mode="after")
    # def search_path_exists(cls, value: Path) -> None:
    #     """
    #     Check if the path exists
    #     """
    #     # Check if the path exists
    #     if not value.exists():
    #         raise ValueError(f"{value} doesn't exist.")

    # @field_validator('user_search_input', mode="after")
    # def search_path_valid(cls, value: Path) -> None:
    #     # Prevent directory traversal attacks
    #     doccli_base_dir: Path = Path(os.getenv("DOCCLI_BASE_DIR"))
    #     if str(doccli_base_dir.resolve()) not in str(value.resolve()):
    #         raise ValueError(f"The search path {value.resolve()} is outside the base directory configured by the administrator.")
