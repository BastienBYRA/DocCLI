import os

from shared.configs.base_config import BaseConfig
from shared.configs.git_config import GitConfig
from shared.configs.os_config import OsConfig
from shared.enums.execution_mode import ExecutionMode
from shared.enums.source_type import SourceType
from shared.services.git_service import GitService
from shared.validators.base_validator import BaseValidator


class ApplicationConfig:
    """
    Helper class to get various configurations related to the application configuration.
    """

    def get_execution_mode() -> ExecutionMode:
        """
        Get the execution mode of the program (Client, Server, or Client-Server mode).
        """

        if not BaseValidator.validate_doccli_mode():
            exit(1)

        doccli_mode = os.getenv("DOCCLI_MODE").lower()

        try:
            return ExecutionMode(doccli_mode)
        except ValueError:
            raise ValueError("DOCCLI_MODE is incorrect, expected values: client-server, client or server")

    
    def get_doccli_config() -> BaseConfig:
        """
        Get the mode used to run the program; Client, Server or Client-Server 
        """
        if not BaseValidator.validate_doccli_source():
            exit(1)
            
        # Get and valid the SEARCH_SOURCE variable
        doccli_source = os.getenv("DOCCLI_SOURCE").lower()
        config: BaseConfig
        match SourceType(doccli_source):
            case SourceType.OS:
                config = OsConfig.create_from_env()
            case SourceType.GIT:
                config = GitConfig.create_from_env()
                GitService(git_config=config).clone_repo()
            case _:
                raise ValueError("The source specified in DOCCLI_SOURCE is unknown. Expected values: os, git")
        
        return config
    

    def verify_client_server() -> None:
        BaseValidator.validate_server()
        return

    def verify_server() -> None:
        BaseValidator.validate_server()
        return

    def verify_client():
        BaseValidator.validate_client()
        return