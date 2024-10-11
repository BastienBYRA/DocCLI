import os

from models.git_config import GitConfig
from models.os_config import OsConfig
from models.source_config import SourceConfig

def is_env_empty(env: str) -> bool:
    """
    Check if an environment variable is empty
    """

    value = os.getenv(env)
    if value:
        return True
    return False
    
def get_base_env() -> SourceConfig:
    """
    Return a SourceConfig object with it value filled.
    """

    base_dir = os.getenv("DOCCLI_BASE_DIR")
    return SourceConfig("TEMP", base_dir)

def get_os_env() -> OsConfig:
    """
    Return a OsConfig object with it value filled
    """

    base_config = get_base_env()
    base_dir = base_config.base_dir
    return OsConfig(base_dir)

def get_git_env() -> GitConfig:
    """
    Return a GitConfig object with it value filled
    """

    base_config = get_base_env()

    repo_url = os.getenv("GIT_URL")
    if not repo_url:
            raise ValueError("GIT_URL is not defined.")
    username = os.getenv("GIT_USERNAME")
    password = os.getenv("GIT_PASSWORD")
    branch = os.getenv("GIT_BRANCH")
    base_dir = base_config.base_dir

    return GitConfig(base_dir, repo_url, username, password, branch)