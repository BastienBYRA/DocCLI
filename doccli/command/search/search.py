from pathlib import Path
import re
from typing import List

from models.git_config import GitConfig
from services.git_service import checkout_repo, clone_repo, pull_repo
from models.search_command import SearchCommand

def search_entrypoint_source(search_command: SearchCommand):
    fullpath = Path(search_command.source_config.base_dir + str(search_command.search_path))

    # isinstance so Mypy cease to trigger an error
    if search_command.source_config.source.upper() == "GIT" and isinstance(search_command.source_config, GitConfig):
        clone_repo(search_command.source_config)
        checkout_repo(search_command.source_config)
        pull_repo(search_command.source_config)


    is_file_or_dir(fullpath, search_command.exclude)


def is_file_or_dir(search: Path, exclude: List[str]) -> None:
    """
    Check whether the search input is a file or a directory.

    :param search: The file or directory searched by the user.
    :type search: Path
    :param exclude: The list of regex that search shouldn't match to be valid
    :type exclude: List[str]
    :return: None, print the result.

    :Example:
    >>> is_file_or_dir("/path/to/file/hello.txt")
    "Hello from my file !"
    """

    # Check the path exists
    if not search.exists():
        print(f"{search} does not exist.")
        return None

    # Check if the path is a file or a dir
    if search.is_dir():
        return print_tree_dir(search, exclude)
    else:
        return print_file_content(search, exclude)


def print_tree_dir(search: Path, exclude: List[str]) -> None:

    for line in tree(search, prefix="", exclude=exclude):
        print(line)

    return None


def print_file_content(search: Path, exclude: List[str]) -> None:

    if is_search_excluded(search, exclude) is True:
        return None

    print("Content from : " + str(search))
    print("- * - * - * - * - * - * - * - * -")
    with search.open() as f:
        for line in f:
            print("| " + line, end='')
    print("\n- * - * - * - * - * - * - * - * -")
    return None


# Based on this code : https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def tree(dir_path: Path, exclude: List[str], prefix: str=''):
    """
    A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
   
    # prefix components:
    space =  '    '
    branch = '│   '
    # pointers:
    tee =    '├── '
    last =   '└── '
  
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):

        # Check if the file is to be exclude
        filepath = Path(prefix + pointer + path.name)
        if is_search_excluded(filepath, exclude) is False:
            yield prefix + pointer + path.name

        # Check if the directory is to be exclude
        if path.is_dir() and is_search_excluded(path, exclude) is False: # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension, exclude=exclude)



def is_search_excluded(search: Path, exclude: List[str]) -> bool:
    """
    Checks whether the search should be excluded or not

    :param search: The file or directory searched by the user.
    :type search: Path
    :param exclude: The list of regex that search shouldn't match to be valid
    :type exclude: List[str]
    :return: A bool, True if the search is mean to be exclude, false otherwise.

    :Example:
    >>> is_file_or_dir("/path/to/file/hello.txt", ".*.txt")
    False
    """

    if len(exclude) > 0:
        for reg in exclude:
            if re.search(reg, str(search)) is not None:
                return True
                
    return False