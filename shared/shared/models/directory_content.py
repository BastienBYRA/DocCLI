from dataclasses import dataclass, field
import json
from typing import List
from shared.models.directory_content_option import DirectoryContentOption

@dataclass
class DirectoryContent:
    options: List[DirectoryContentOption] = field(default_factory=list)
    title: str = ""
    can_go_back: bool = False


    def add_option(self, option: DirectoryContentOption):
        self.options.append(option)


    def get_list_options(self) -> list[str]:
        options_list: list[str] = []

        for opt in self.options:
            options_list.append(opt.name)


    def to_json(self):
        return json.loads(json.dumps(self, default=lambda self: self.__dict__))
    
    @staticmethod
    def from_json(data: dict) -> 'DirectoryContent':
        return DirectoryContent(
            options=[DirectoryContentOption.from_json(option) for option in data.get('options', [])],
            title=data.get('title', ''),
            can_go_back=data.get('can_go_back', False)
        )