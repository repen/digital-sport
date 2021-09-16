"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from .abstract import AbstractSport
import requests
from .tool import log
from concurrent.futures import ThreadPoolExecutor


logger = log(__name__)


class FootballSport(AbstractSport):

    def __init__(self, token: str, base_url:str=""):
        self.token = token
        self.limit = -9999

        self.headers = {
            'X-Service-Key': self.token
        }
        if not base_url:
            self.base_url = "https://static.data-provider.ru/api/v1/fsfootball"
        else:
            self.base_url = base_url

    def __len__(self):
        return self.limit

    def _request(self, route: str):
        response = requests.get(self.base_url + route, headers=self.headers)
        if response.status_code == 404:
            raise ValueError(f"Resource [{route}] not found!")
        if response.status_code == 401:
            raise ValueError(f"{response.headers.get('WWW-Authenticate')}")
        self.limit = response.headers.get("X-Service-Limit")
        logger.info(f"Requests limit: {self.limit}")
        return response

    def statistics(self, match_id: str):
        route = "/statistics/" + match_id
        response = self._request(route)
        return response.json()

    def live(self):
        route = "/live"
        response = self._request(route)
        return response.json()

    def odds(self, match_id: str):
        route = "/odds/" + match_id
        response = self._request(route)
        return response.json()

    def h2h(self, match_id: str):
        route = "/h2h/" + match_id
        response = self._request(route)
        return response.json()

    def add_statistics(self, fixtures: list, workers=4) -> list:

        def get_statistics(fixture: dict):
            if fixture['statistics'] != "None":
                data = self.statistics(fixture['statistics'])
                logger.debug(f"Statistics for ID: {fixture['statistics']}. "
                             f"Length: {len(data)}")
                fixture['statistics'] = data

        # Basic
        # for fixture in fixtures:
        #     get_statistics(fixture)

        # Threading
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for _ in executor.map(get_statistics, fixtures):
                pass

        return fixtures