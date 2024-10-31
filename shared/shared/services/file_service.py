from dataclasses import dataclass
from pathlib import Path
import re
from typing import Generator, List

from pandas import DataFrame

from shared.enums.file_type import FileType
from shared.services.file_readers.default_file_reader import DefaultFileReader
from shared.services.file_readers.excel_file_reader import ExcelFileReader
from shared.services.file_readers.pdf_file_reader import PdfFileReader

class FileService():
    """Classe utilitaire pour gérer des fichiers. Contient uniquement des méthodes statiques."""

    # def __init__(self) -> None:
    #     raise NotImplementedError("Cette classe ne doit pas être instanciée.")

    @staticmethod
    def path_exist(search: Path) -> bool:
        print(f"Est-ce que ca existe ? : {search.exists()}")
        if not search.exists() :
            print(f"{search} does not exist.")
            return False
        return True
    
    @staticmethod
    def is_path_excluded(search: Path, exclude_list: List[str]) -> bool:
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

        if len(exclude_list) > 0:
            for reg in exclude_list:
                if re.search(reg, str(search)) is not None:
                    return True
                    
        return False

    @staticmethod
    def is_folder(search: Path) -> bool:
        return search.is_dir()
    
    @staticmethod
    def read_file(search: Path) -> None:
        file_content: str | DataFrame = ""
        filetype: str = ""

        if len(search.suffixes) == 0:
            raise ValueError(f"The file {search} has no suffix.")

        if len(search.suffixes) > 1:
            print(f"The file {search} has several suffixes, only the last one is taken into account")
            filetype = search.suffixes[-1]
        else:
            filetype = search.suffix
        
        match FileType(filetype):
            case FileType.EXCEL:
                file_content = ExcelFileReader.read(search)
            # case FileType.WORD:
            #     file_content = WordFileReader.read(search)
            case FileType.PDF:
                file_content = PdfFileReader.read(search)
            case _:
                file_content = DefaultFileReader.read(search)

        print(file_content)
    
    
    def tree_folder(self, search: Path, exclude_list: List[str]) -> None:
        for line in self.tree(search, prefix="", exclude_list=exclude_list):
            print(line)
    
    @staticmethod
    def is_search_excluded(search: Path, exclude: List[str]) -> bool:
        """
        Checks whether the search should be excluded or not

        :param search: The file or directory searched by the user.
        :type search: Path
        :param exclude: The list of regex that search shouldn't match to be valid
        :type exclude: List[str]
        :return: A bool, True if the search is mean to be exclude, false otherwise.

        :Example:
        >>> is_search_excluded("/path/to/file/hello.txt", ".*.txt")
        True
        """

        if len(exclude) > 0:
            for reg in exclude:
                if re.search(reg, str(search)) is not None:
                    return True
                    
        return False
            
    # Based on this code : https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    def tree(self, dir_path: Path, exclude_list: List[str], prefix: str = '') -> Generator[str, None, None]:
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
            if self.is_search_excluded(filepath, exclude_list) is False:
                yield prefix + pointer + path.name

            # Check if the directory is to be exclude
            if path.is_dir() and self.is_search_excluded(path, exclude_list) is False: # extend the prefix and recurse:
                extension = branch if pointer == tee else space 
                # i.e. space because last, └── , above so no more |
                yield from self.tree(path, prefix=prefix+extension, exclude_list=exclude_list)


    # def is_folder_or_file(this, search: Path):
    #     """
    #     Check whether the search input is a file or a directory.

    #     :param search: The file or directory searched by the user.
    #     :type search: Path
    #     :return: None, print the result.

    #     :Example:
    #     >>> is_file_or_dir("/path/to/file/hello.txt")
    #     "Hello from my file !"
    #     """

    #     # Check the path exists
    #     if not search.exists():
    #         print(f"{search} does not exist.")
    #         return None

    #     # Check if the path is a file or a dir
    #     if search.is_dir():
    #         return this.tree_folder(search, exclude)
    #     else:
    #         return this.read_file(search, exclude)