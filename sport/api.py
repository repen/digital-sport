"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from .abstract import AbstractSport
import requests
from .tool import log
from concurrent.futures import ThreadPoolExecutor


logger = log(__name__)


_FOOTBALL_URL = "https://static.data-provider.ru/api/v1/fsfootball"
_BASKETBALL_URL = "https://static.data-provider.ru/api/v1/fsbasketball"
_TENNIS_URL = "https://static.data-provider.ru/api/v1/fstennis"


class FootballSport(AbstractSport):

    def __init__(self, token: str, debug=False):
        self.request_limit = None
        self.reset_limit = None
        self.token = token
        self.debug = debug
        self.headers = {
            'X-Service-Key': self.token
        }
        self.base_url = _FOOTBALL_URL

    def __len__(self):
        return self.request_limit

    def _request(self, route: str):
        response = requests.get(self.base_url + route, headers=self.headers)
        if response.status_code == 404:
            raise ValueError(f"Resource [{route}] not found!")
        if response.status_code == 401:
            raise ValueError(f"{response.headers.get('WWW-Authenticate')}")
        self.request_limit = response.headers.get("X-Day-Limit-Value")
        self.reset_limit = response.headers.get("X-Day-Limit-Reset")
        if self.debug:
            logger.info(f"Requests limit: {self.request_limit}")
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
                if self.debug:
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


class BasketballSport(FootballSport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = _BASKETBALL_URL


class TennisSport(FootballSport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = _TENNIS_URL