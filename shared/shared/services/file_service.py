from dataclasses import dataclass
from pathlib import Path
import re
from typing import Generator, List
from pick import pick

from pandas import DataFrame

from shared.enums.file_type import FileType
from shared.enums.search_response_type import SearchResponseType
from shared.models.file_content import FileContent
from shared.models.search import Search
from shared.models.search_result import SearchResult
from shared.services.file_readers.default_file_reader import DefaultFileReader
from shared.services.file_readers.excel_file_reader import ExcelFileReader
from shared.services.file_readers.pdf_file_reader import PdfFileReader
from shared.configs.base_config import BaseConfig
from shared.models.directory_content_option import DirectoryContentOption
from shared.models.directory_content import DirectoryContent

class FileService:
    """Classe utilitaire pour gérer des fichiers. Contient uniquement des méthodes statiques."""

    # def __init__(self) -> None:
    #     raise NotImplementedError("Cette classe ne doit pas être instanciée.")

    @staticmethod
    def path_exist(search: Path) -> bool:
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
        exist = search.exists()
        if exist is False:
            ValueError("There is no file nor folder.")
        return search.is_dir()
    
    @staticmethod
    def read_file(search: Path) -> SearchResult:
        file_content: str | DataFrame = ""
        filetype: str = ""

        if len(search.suffixes) == 0:
            raise ValueError(f"The file {search} has no suffix, default to .txt behavior.")

        if len(search.suffixes) > 1:
            print(f"The file {search} has several suffixes, only the last one is taken into account")
            filetype = search.suffixes[-1]
        else:
            filetype = search.suffix
        
        match filetype:
            case FileType.EXCEL:
                file_content = ExcelFileReader.read(search)
            # case FileType.WORD:
            #     file_content = WordFileReader.read(search)
            case FileType.PDF:
                file_content = PdfFileReader.read(search)
            case _:
                file_content = DefaultFileReader.read(search)

        file_content: FileContent = FileContent(search.name, file_content)
        return SearchResult(SearchResponseType.FILE, file_content, None)
    
    
    def tree_folder(search_path: Path, base_dir_path: str) -> SearchResult:

        # Make sure the user don't go outside the base directory defined
        can_go_back = False
        if str(Path(base_dir_path).resolve()) in str(search_path.resolve()) and str(Path(base_dir_path).resolve()) != str(search_path.resolve()):
            can_go_back = True

        # Récupère la liste des fichiers
        contents = search_path.iterdir()

        # Parcours la liste des fichiers, si on trouve un fichier, l'ajoute à la liste, si dossier, l'ajouter à la liste avec "/" à la fin
        title = 'Choose the file or folder you want to see the content: '
        options = []

        for result in contents:
            if result.is_dir():
                options.append(f"{result.name}/")
            else:
                options.append(result.name)

        # Make sure the user don't go outside the base directory defined
        if can_go_back is True:
            options.append("Go back")
        options.append("Quit")

        if len(options) <= 2:
            title = "There is no files nor folders in the directory :"

        # Ajoute les options à un objet DirectoryContent
        directory_content: DirectoryContent = DirectoryContent([], title, can_go_back)
        for index in range(len(options)):
            directory_content_opt: DirectoryContentOption = DirectoryContentOption(index, options[index])
            directory_content.add_option(directory_content_opt)

        return SearchResult(SearchResponseType.DIRECTORY, None, directory_content)
        
    
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





    # # Based on this code : https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    # def tree(self, dir_path: Path, exclude_list: List[str], prefix: str = '') -> Generator[str, None, None]:
    #     """
    #     A recursive generator, given a directory Path object
    #     will yield a visual tree structure line by line
    #     with each line prefixed by the same characters
    #     """
    #     # prefix components:
    #     space =  '    '
    #     branch = '│   '
    #     # pointers:
    #     tee =    '├── '
    #     last =   '└── '

    #     contents = list(dir_path.iterdir())
    #     # contents each get pointers that are ├── with a final └── :
    #     pointers = [tee] * (len(contents) - 1) + [last]
    #     for pointer, path in zip(pointers, contents):

    #         # Check if the file is to be exclude
    #         filepath = Path(prefix + pointer + path.name)
    #         if self.is_search_excluded(filepath, exclude_list) is False:
    #             yield prefix + pointer + path.name

    #         # Check if the directory is to be exclude
    #         if path.is_dir() and self.is_search_excluded(path, exclude_list) is False: # extend the prefix and recurse:
    #             extension = branch if pointer == tee else space 
    #             # i.e. space because last, └── , above so no more |
    #             yield from self.tree(path, prefix=prefix+extension, exclude_list=exclude_list)


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