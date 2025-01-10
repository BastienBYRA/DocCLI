from dataclasses import dataclass


@dataclass
class DirectoryContentOption:
    index: int = -1
    name: str = ""


    @staticmethod
    def from_json(data: dict) -> 'DirectoryContentOption':
        return DirectoryContentOption(
            index=data.get('index', -1),
            name=data.get('name', '')
        )