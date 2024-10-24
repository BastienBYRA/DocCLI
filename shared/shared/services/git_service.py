from shared.shared.configs.git_config import GitConfig
from git import Repo, GitCommandError

class GitService:
    def __init__(self, git_config: GitConfig):
        """
        Initialize the GitService with the provided configuration.

        :param git_config: Configuration object containing Git details such as the repo URL, credentials, and base directory.
        :type git_config: GitConfig
        :return: None

        :Example:
        >>> config = GitConfig(repo_url="https://github.com/user/repo.git", base_dir="/path/to/dir", branch="main")
        >>> git_service = GitService(config)
        """
        self.git_config = git_config

    def clone_repo(self):
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
        git_password = self.git_config.password

        if not repo_url:
            raise ValueError("GIT_URL is not defined.")

        if (not git_username and git_password) or (git_username and not git_password):
            raise ValueError("Either the git username or password is defined. Define both or none.")

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

    def pull_repo(self):
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

    def checkout_repo(self):
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
