import os
from typing import Optional, Self, cast, override
from pydantic import Field, field_validator, model_validator

from shared.configs.base_config import BaseConfig
from shared.enums.source_type import SourceType

class GitConfig(BaseConfig):
    source: SourceType = Field(SourceType.GIT, frozen=True)
    repo_url: str
    username: Optional[str] = None
    token: Optional[str] = None
    branch: str = "main"

    @override
    @classmethod
    def create_from_env(cls) -> Self:
        """
        Return a OsConfig object with its values filled from environment variables.
        """
        base_dir = cast(str, os.getenv("DOCCLI_BASE_DIR"))
        repo_url = cast(str, os.getenv("GIT_URL"))
        username = cast(str, os.getenv("GIT_USERNAME"))
        token = cast(str, os.getenv("GIT_TOKEN"))
        branch = cast(str, os.getenv("GIT_BRANCH"))
        
        return cls(source=SourceType.GIT, base_dir=base_dir, repo_url=repo_url, username=username, token=token, branch=branch)

    @field_validator("repo_url")
    @classmethod
    def validate_repo_url(cls, v: str) -> str:
        if not v:
            raise ValueError("GIT_URL is not defined.")
        return v
    
    @model_validator(mode="after")
    def validate_username_token(self) -> Self:
        username = self.username
        token = self.token
        
        if (not username and token) or (username and not token):
            raise ValueError("Both GIT_USERNAME and GIT_token must be defined together, or neither.")
        return self
    
    @field_validator("branch")
    @classmethod
    def set_default_branch(cls, v: Optional[str]) -> str:
        return v or "main"

