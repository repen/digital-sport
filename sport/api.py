"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from typing import List
from .abstract import AbstractSport
import requests
from .tool import log
from .search_center import H2hSearch, SearchStatistics
from .report_service import ReportService
from .interface import IStatistics
from concurrent.futures import ThreadPoolExecutor

import requests_cache
requests_cache.install_cache()


logger = log(__name__)

_FOOTBALL_URL = "https://static.data-provider.ru/api/v1/fsfootball"
_BASKETBALL_URL = "https://static.data-provider.ru/api/v1/fsbasketball"
_TENNIS_URL = "https://static.data-provider.ru/api/v1/fstennis"


class ListWrapper(list):
    def __init__(self, ll, method_name, cls):
        super(ListWrapper, self).__init__(ll)
        self.method_name = method_name
        self.cls = cls

    def search_statistics(self, name_statistics, period=None, expression=None, function=None):
        if self.method_name == "statistics":
            i_statistics:List[IStatistics]  = [IStatistics(**x) for x in self]
            SearchStatistics(i_statistics, name_statistics, period, expression, function).run()

        if self.method_name == "live":
            for item in self:
                if item['statistics'] == "None":
                    continue
                i_statistics = [IStatistics(**x) for x in self.cls.statistics(item['match_id'])]
                SearchStatistics(i_statistics, name_statistics, period, expression, function).run()



    def search_last_result(self, *args, **kwargs):
        if self.method_name == "h2h":
            H2hSearch(self, self.cls).h2h_search_last_result(*args, **kwargs)
        if self.method_name == "live":
            H2hSearch(self, self.cls).live_search_last_result(*args, **kwargs)

    def csv_dump(self, *args, **kwargs):
        return ReportService(self).csv_dump(*args, **kwargs)

    def json_dump(self, *args, **kwargs):
        return ReportService(self).json_dump(*args, **kwargs)


def list_wrapper(name):

    def _list_wrapper(f):

        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            Self = args[0]
            report_list = ListWrapper(res, name, Self)
            return report_list

        return wrapper

    return _list_wrapper


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

    @list_wrapper("statistics")
    def statistics(self, match_id: str):
        route = "/statistics/" + match_id
        response = self._request(route)
        return response.json()

    @list_wrapper("live")
    def live(self):
        route = "/live"
        response = self._request(route)
        return response.json()

    @list_wrapper("odds")
    def odds(self, match_id: str):
        route = "/odds/" + match_id
        response = self._request(route)
        return response.json()

    @list_wrapper("h2h")
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