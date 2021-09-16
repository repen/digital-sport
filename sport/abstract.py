"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import abc


class AbstractSport(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, token: str):
        self.token = token

    @abc.abstractmethod
    def _request(self, route: str):
        pass

    @abc.abstractmethod
    def live(self):
        pass

    @abc.abstractmethod
    def statistics(self, match_id: str):
        pass

    @abc.abstractmethod
    def odds(self, match_id: str):
        pass

    @abc.abstractmethod
    def h2h(self, match_id: str):
        pass

    @abc.abstractmethod
    def __len__(self):
        """Limit api"""
        pass

