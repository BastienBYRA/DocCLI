from pathlib import Path

def is_file_or_dir(search: Path) -> None:
    """
    Check whether the search input is a file or a directory.

    :param search: The file or directory searched by the user.
    :type search: Path
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
        return print_tree_dir(search)
    else:
        return print_file_content(search)


def print_tree_dir(search: Path) -> None:
    for line in tree(search):
        print(line)
    return None

def print_file_content(search: Path) -> None:
    print("Content from : " + str(search))
    print("- * - * - * - * - * - * - * - * -")
    with search.open() as f:
        for line in f:
            print("| " + line, end='')
    print("\n- * - * - * - * - * - * - * - * -")
    return None


# https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def tree(dir_path: Path, prefix: str=''):
    # prefix components:
    space =  '    '
    branch = '│   '
    # pointers:
    tee =    '├── '
    last =   '└── '

    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)