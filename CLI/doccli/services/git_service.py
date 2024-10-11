from git import GitCommandError, InvalidGitRepositoryError, Repo

from models.git_config import GitConfig

def clone_repo(git_config: GitConfig):
    repo_url = git_config.repo_url
    git_username = git_config.username
    git_password = git_config.password
    base_dir = git_config.base_dir

    if not repo_url:
        print("GIT_URL is not defined.")

    # If one is defined but not the other
    if (not git_username and git_password) or (git_username and not git_password):
        print("Either the git username of password is defined, define both or none.")
    
    try:
        Repo.clone_from(repo_url, base_dir)
    except GitCommandError as e:
        # Vérifier si l'erreur est celle liée à un répertoire non vide
        if "already exists and is not an empty directory" in str(e):
            pass
        else:
            raise e
    except Exception as e:
        raise e

def pull_repo(git_config: GitConfig):
    base_dir = git_config.base_dir

    repo = Repo(base_dir)
    repo.remotes.origin.pull()

def checkout_repo(git_config: GitConfig):
    base_dir = git_config.base_dir
    branch = git_config.branch

    repo = Repo(base_dir)
    repo.git.checkout(branch)