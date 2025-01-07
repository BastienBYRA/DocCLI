from pathlib import Path
from pick import pick

from shared.models.directory_content import DirectoryContent
from shared.models.search import Search
from shared.models.search_result import SearchResult
from shared.services.file_service import FileService


class CLI:

    def choose_pick_cli(result: SearchResult, search_input: str) -> str:
        directory: DirectoryContent = result.directory_content

        options = []
        for opt in directory.options:
            options.append(opt.name)

        title = directory.title
        can_go_back = directory.can_go_back

        # Ask the user to choose the file/directory to browse
        option, index = pick(options, title)
        new_search: Path

        # If "Quit"
        if index == len(options) - 1:
            exit(0)
        # If Go Back
        elif index == len(options) - 2 and can_go_back is True:
            new_search = "/".join(search_input.rstrip("/").split("/")[:-1])
            return new_search
        else:
            new_search = search_input + option
            return new_search
        

    def choose_pick(result: SearchResult, search: Search, base_dir: str) -> SearchResult:
        directory: DirectoryContent = result.directory_content

        options = []
        for opt in directory.options:
            options.append(opt.name)

        title = directory.title
        can_go_back = directory.can_go_back

        # Ask the user to choose the file/directory to browse
        option, index = pick(options, title)
        new_search: Path

        # If "Quit"
        if index == len(options) - 1:
            exit(0)
        # If Go Back
        elif index == len(options) - 2 and can_go_back is True:
            new_search = Path(search.search_path.parent)
            search.search_path = new_search
            return FileService.tree_folder(search, base_dir)
        # Check folder
        elif option[-1] == "/":
            new_search = Path.joinpath(search.search_path, option)
            search.search_path = new_search
            return FileService.tree_folder(search, base_dir)
        # Check file
        else:
            new_search = Path.joinpath(search.search_path, option)
            return FileService.read_file(new_search)