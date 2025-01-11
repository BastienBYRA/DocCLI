

import json
import requests

from doccli.models.search_result import SearchResult


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