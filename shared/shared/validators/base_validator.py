import os
from pathlib import Path
from shared.enums.execution_mode import ExecutionMode
from shared.enums.source_type import SourceType
from shared.helpers.environment_variable_helper import EnvironmentVariableHelper


class BaseValidator:
    """
    A base class for validating shared / common components across the program.
    """

    @staticmethod
    def validate_server() -> bool:
        BaseValidator.validate_doccli_mode()
        BaseValidator.validate_doccli_source()
        BaseValidator.validate_doccli_base_dir()
        return True
    
    @staticmethod
    def validate_client() -> bool:
        BaseValidator.validate_doccli_mode()
        return True

    @staticmethod
    def validate_doccli_mode() -> bool:
        """
        Validates the environment variable 'DOCCLI_MODE' to ensure it meets the expected criteria.
        
        This function performs the following checks:
        1. Verifies that the environment variable 'DOCCLI_MODE' is defined.
        2. Validates that the value of 'DOCCLI_MODE' matches the expected options ('client', 'server' or 'client-server').

        :return: True if all checks pass.
        :raises ValueError: If the variable is not defined, has an invalid value, or poses a security risk.
        """
        # Check DOCCLI_MODE is defined
        doccli_mode_exist: bool = EnvironmentVariableHelper.variable_exists("DOCCLI_MODE")
        if doccli_mode_exist is False:
            raise ValueError("DOCCLI_MODE is not defined.")

        # Check the value is valid
        doccli_mode = os.getenv("DOCCLI_MODE")
        doccli_mode_valid = EnvironmentVariableHelper.variable_valid(doccli_mode, ExecutionMode)
        if doccli_mode_valid is False:
            raise ValueError("The DOCCLI_MODE specified is unknown. Expected values: client, server, client-server")
        
        return True
    

    def validate_doccli_source() -> bool:
        """
        Validates the environment variable 'DOCCLI_SOURCE' to ensure it meets the expected criteria.
        
        This function performs the following checks:
        1. Verifies that the environment variable 'DOCCLI_SOURCE' is defined.
        2. Validates that the value of 'DOCCLI_SOURCE' matches the expected options (e.g: 'os', 'git').

        :return: True if all checks pass.
        :raises ValueError: If the variable is not defined, has an invalid value, or poses a security risk.
        """
        # Check DOCCLI_SOURCE is defined
        doccli_source_exist: bool = EnvironmentVariableHelper.variable_exists("DOCCLI_SOURCE")
        if doccli_source_exist is False:
            raise ValueError("DOCCLI_SOURCE is not defined.")

        # Check the value is valid
        doccli_source = os.getenv("DOCCLI_SOURCE")
        doccli_source_valid = EnvironmentVariableHelper.variable_valid(doccli_source, SourceType)
        if doccli_source_valid is False:
            raise ValueError("The DOCCLI_SOURCE specified is unknown. Expected values: os, git")
        
        return True
    

    def validate_doccli_base_dir() -> bool:
        """
        Validates the environment variable 'DOCCLI_BASE_DIR' to ensure it meets the expected criteria.
        
        This function performs the following checks:
        1. Verifies that the environment variable 'DOCCLI_BASE_DIR' is defined.
        2. Validates that the value of 'DOCCLI_BASE_DIR' points to a valid directory path.

        :return: True if all checks pass.
        :raises ValueError: If the variable is not defined or its value is invalid (e.g., the path is incorrect).
        """

        # Check DOCCLI_BASE_DIR is defined
        doccli_base_dir_exist: bool = EnvironmentVariableHelper.variable_exists("DOCCLI_BASE_DIR")
        if doccli_base_dir_exist is False:
            raise ValueError("DOCCLI_BASE_DIR is not defined.")
        
        # Check the value is valid
        doccli_base_dir = os.getenv("DOCCLI_BASE_DIR")
        doccli_base_dir_valid = EnvironmentVariableHelper.variable_valid(doccli_base_dir, Path)
        if doccli_base_dir_valid is False:
            raise ValueError("The directory DOCCLI_BASE_DIR defined is incorrect.")

        return True