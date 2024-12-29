from pathlib import Path
from pick import pick

from shared.commands.search import Search
from shared.models.file_content import FileContent
from shared.models.tree_picker import TreePicker
from shared.services.file_service import FileService


class CLI:

    def choose_pick(picker: TreePicker) -> TreePicker | FileContent:
        file_service: FileService = FileService()

        options = []
        for opt in picker.options:
            options.append(opt.name)

        title = picker.title
        can_go_back = picker.can_go_back
        search = picker.search
        exclude_list = picker.exclude_list
        config = picker.config

        option, index = pick(options, title)
        new_search: Path

        # If "Quit"
        if index == len(options) - 1:
            exit(0)
        # If Go Back
        elif index == len(options) - 2 and can_go_back is True:
            new_search = Path(search.parent)
            return file_service.tree_folder(new_search, exclude_list, config)
        # Check folder
        elif option[-1] == "/":
            new_search = Path.joinpath(search, option)
            return file_service.tree_folder(new_search, exclude_list, config)
        # Check file
        else:
            new_search = Path.joinpath(search, option)
            return file_service.read_file(new_search)