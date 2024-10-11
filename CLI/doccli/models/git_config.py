from typing import Optional
from models.source_config import SourceConfig


class GitConfig(SourceConfig):
    def __init__(self, base_dir: str, repo_url: str, username: Optional[str] = None, password: Optional[str] = None, branch: Optional[str] = "main") -> None:
        super().__init__(source="git", base_dir=base_dir)

        if not repo_url:
            raise ValueError("GIT_URL is not defined.")
        
        if (not username and password) or (username and not password):
            raise ValueError("Both GIT_USERNAME and GIT_PASSWORD must be defined together, or neither.")
        
        if not branch:
            branch = "main"
        
        self.repo_url = repo_url
        self.username = username
        self.password = password
        self.branch = branch