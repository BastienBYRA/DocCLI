from doccli.configs.git_config import GitConfig
from git import Repo, GitCommandError
from pydantic import BaseModel

class GitService(BaseModel):
    git_config: GitConfig   # Configuration object containing Git details such as the repo URL, credentials, and base directory.

    def clone_repo(self) -> None:
        """
        Clone the repository from the URL specified in the configuration.
        If the repository already exists, it will skip the cloning process.
        After cloning, it checks out to the specified branch and pulls the latest changes.

        :return: None

        :Example:
        >>> git_service.clone_repo()
        Cloning repository from https://github.com/user/repo.git into /path/to/dir...
        Repository already exists at /path/to/dir.
        """
        repo_url = self.git_config.repo_url
        base_dir = self.git_config.base_dir
        git_username = self.git_config.username
        git_token = self.git_config.token

        if (git_username and git_token):
            self.login()

        try:
            print(f"Cloning repository from {repo_url} into {base_dir}...")
            Repo.clone_from(repo_url, base_dir)
        except GitCommandError as e:
            if "already exists and is not an empty directory" in str(e):
                print(f"Repository already exists at {base_dir}.")
            else:
                raise e
        except Exception as e:
            raise RuntimeError(f"Error while cloning the repository: {e}")

        self.checkout_repo()
        self.pull_repo()

    def login(self) -> bool:
        """
        Authenticate with Git using the username and token provided in the configuration.

        This method logs into the Git service using the credentials stored in the 
        configuration. If both username and token are available, it will attempt 
        authentication. If successful, it enables authenticated Git operations 
        such as cloning and pulling from private repositories. 

        Note:
        This method must be implemented to handle the specific authentication 
        mechanism required (e.g., configuring Git credentials, setting up a credential 
        helper, or using an API token instead of a token).

        :return: True if login is successful, False otherwise.

        :Example:
        >>> git_service.login()
        Successfully authenticated with Git.
        """
        #raise NotImplementedError("The method login is not implemented yet.")
        print("[WARNING]: The method login is not implemented yet, you will not be authentified.")
        return False


    def pull_repo(self) -> None:
        """
        Pull the latest changes from the remote repository's origin branch.

        :return: None

        :Example:
        >>> git_service.pull_repo()
        Pulling the latest changes...
        """
        base_dir = self.git_config.base_dir
        try:
            repo = Repo(base_dir)
            print("Pulling the latest changes...")
            repo.remotes.origin.pull()
        except Exception as e:
            raise RuntimeError(f"Error while pulling the repository: {e}")

    def checkout_repo(self) -> None:
        """
        Checkout to the branch specified in the configuration.
        This will ensure that the repository is on the correct branch before pulling changes.

        :return: None

        :Example:
        >>> git_service.checkout_repo()
        Checking out to branch main...
        """
        base_dir = self.git_config.base_dir
        branch = self.git_config.branch

        try:
            repo = Repo(base_dir)
            print(f"Checking out to branch {branch}...")
            repo.git.checkout(branch)
        except Exception as e:
            raise RuntimeError(f"Error while checking out branch {branch}: {e}")
