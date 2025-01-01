from dataclasses import dataclass
from pathlib import Path

from shared.models.file_content import FileContent
from shared.models.directory_content import DirectoryContent


@dataclass
class SearchResult:
    # type: str = "TODO"
    file_content: FileContent | None
    directory_content: DirectoryContent | None

    def is_valid(self):
        if (self.file_content is None and self.directory_content is None) or (self.file_content and self.directory_content):
            return False
        return True
    
    def get_file_content(self):
        if not self.file_content:
            raise ValueError("The result doesn't have a file content")

        return FileContent.content
    
    def get_directory_content(self):
        if not self.directory_content:
            raise ValueError("The result doesn't have a tree picker")
        
        return self.directory_content.get_list_options()
    
    def print_file_content(self):
        print("-------------- START CONTENT --------------")
        print(self.file_content.content)
        print("--------------- END CONTENT ---------------")
