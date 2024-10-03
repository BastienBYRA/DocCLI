import os
from git import Repo

# global scope
repo_url = os.environ.get("GIT_URL")
git_username = os.environ.get("GIT_USERNAME")
git_password = os.environ.get("GIT_PASSWORD")

def clone_repo():
    if repo_url is None:
        print("GIT_URL is not defined.")

    # If one is defined but not the other
    if git_username is None and git_password is not None or git_username is not None and git_password is None:
        print("Either the git username of password is defined, define both or none.")
    
    Repo.clone_from(repo_url, local_dir)

def pull_repo():

    if repo_url is None:
        print("GIT_URL is not defined.")

    repo = Repo(repo_url)
    repo.remotes.origin.pull()