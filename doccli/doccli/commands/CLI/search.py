

import json
from pathlib import Path
import requests

from doccli.models.directory_content import DirectoryContent
from doccli.models.search_result import SearchResult
from pick import pick

class CLISearch():

    @staticmethod
    def run(api_endpoint: str = "", search_input: str = "/", exclude_list: str = "") -> SearchResult:

        if not api_endpoint:
            raise ValueError("No DOCCLI_ENDPOINT found.")

        try:
            response = requests.get(f'{api_endpoint}/search?search_input={search_input}')

            if response.status_code != 200:
                raise ValueError(f"The API didn't return a 200 HTTP Code; {response.status_code}, {response.content}")

            response_content = json.loads(response.content)
            search_result = SearchResult.from_json(response_content)

            return search_result
        except Exception as e:
            raise ValueError(f"An error occured during the request to the API for the 'Search' command; {e}")
        
    @staticmethod
    def local_run():
        raise ValueError("[CLI/SEARCH - LOCAL_RUN] not implemented.")
    
    @staticmethod
    def picker(result: SearchResult, search_input: str) -> str:
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
            # Check last character is "/"
            if search_input.endswith('/'):
                # e.g => /this/is/my/path/ become /this/is/my/
                new_search = search_input.rstrip('/').rsplit('/', 1)[0] + "/"
            else:
                # e.g => /this/is/my/path become /this/is/my/
                new_search = search_input.rsplit('/', 1)[0] + "/"
            return new_search
        else:
            new_search = search_input + option
            return new_search
