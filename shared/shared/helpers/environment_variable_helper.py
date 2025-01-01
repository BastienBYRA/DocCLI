from enum import Enum
import os
from pathlib import Path

from shared.helpers.enum_helper import value_in_enum

class EnvironmentVariableHelper:
    """
    Helper class to manage and validate environment variables.
    """

    @staticmethod
    def variable_exists(env_var: str) -> bool:
        """
        Check if the environment variable exists and has a value.

        :param env_var: Name of the environment variable
        :return: True if the variable exists, False otherwise
        """
        checker: str = os.getenv(env_var)
        if not checker:
            return False
        return True
    
    def variable_valid(env_var: str, validator: object) -> bool:
        """
        Check if the environment variable has a correct value.

        :param env_var: Name of the environment variable
        :param validator: Type of the validator (Your enum, int, str... to compare against the `env_var`)
        :return: True if the variable exists, False otherwise
        """
        is_valid: bool = False
        # Compare `env_var` against a Enum
        if issubclass(validator, Enum):
            is_valid = value_in_enum(env_var, validator)
        # Check `env_var` is a Path
        elif isinstance(validator, Path):
            is_valid = Path(env_var).exists()
        # elif isinstance(validator, int):
        #     is_valid = (int(env_var) == int(validator))
        # elif isinstance(validator, str):
        #     is_valid = (str(env_var) == str(validator))
        else:
            raise ValueError(f"The validator type used is not handled by the application, validator type: {validator}")
        
        return is_valid