from dataclasses import dataclass, field
from typing import List
from shared.configs.base_config import BaseConfig
from shared.models.tree_picker_option import TreePickerOption

@dataclass
class TreePicker:
    options: List[TreePickerOption] = field(default_factory=list)
    title: str = ""
    can_go_back: bool = False
    search: str = None
    exclude_list: List[str] = None
    config: BaseConfig = None

    def add_option(self, option: TreePickerOption):
        self.options.append(option)
