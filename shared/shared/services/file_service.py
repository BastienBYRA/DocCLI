from pathlib import Path
import re
from typing import List

from shared.enums.file_type import FileType
from shared.services.file_readers.default_file_reader import DefaultFileReader
from shared.services.file_readers.excel_file_reader import ExcelFileReader
from shared.services.file_readers.pdf_file_reader import PdfFileReader
from shared.services.file_readers.word_file_reader import WordFileReader


class FileService():
    
    def path_exist(self, search: Path):
        if search.exists() :
            print(f"{search} does not exist.")
            return False
        return True
    
    def is_path_excluded(search: Path, exclude_list):
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

    def is_folder(self, search: Path) -> bool:
        if self.path_exist(search) is False:
            return None
        return self.search.is_dir()
            

    def is_folder_or_file(this, search: Path):
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
            return this.tree_folder(search, exclude)
        else:
            return this.read_file(search, exclude)
    
    def read_file(search: Path, exclude: List[str]):
        file_content: str = ""
        filetype: str = ""

        if len(search.suffix is None):
            raise ValueError(f"The file {search} has no suffix.")


        if len(search.suffixes > 1):
            print(f"The file {search} has several suffixes, only the last one is taken into account")
            filetype = search.suffixes[0]
        else:
            filetype = search.suffix
        
        match FileType(filetype):
            case FileType.EXCEL:
                file_content = ExcelFileReader.read()
            case FileType.WORD:
                file_content = WordFileReader.read()
            case FileType.PDF:
                file_content = PdfFileReader.read()
            case _:
                file_content = DefaultFileReader.read()

        print(file_content)
    
    def tree_folder(search: Path, exclude: List[str]):
        raise Exception
    
    def exclude_filter(search: Path, exclude: List[str]):
        raise Exception