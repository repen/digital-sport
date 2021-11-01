from typing import Callable, List
from .interface import Ih2h
from functools import partial

def pprint(string, match_id:str):
    if match_id:
        string = f"{match_id}: {string}"
    print(string)


class H2hSearch:

    def search_last_result(self, pattern, team="", function:Callable=pprint):
        if self.method_name == "h2h":
            self.h2h_search_last_result(pattern, team, function)
        if self.method_name == "live":
            self.live_search_last_result(pattern, team, function)

    def live_search_last_result(self, pattern, team, function):
        fixtures = [x for x in self]

        for fixture in fixtures:
            h2h_list = self.cls.h2h(fixture['match_id'])
            h2h_list.search_last_result(pattern, team, partial(function, match_id=fixture['match_id']))


    def get_result_h2h(self, team_name,
                   pattern, h2h_list: List[Ih2h], function):
        template = "Found! Team [{team}] [pattern:{pattern}] [{place} games]"
        place = ""
        h2h_list = [x for x in h2h_list if x.match_type == team_name]
        if ":" in pattern:
            place = pattern.split(":")[-1]
            h2h_list = [x for x in h2h_list if x.place == place]
        result = self._h2h_search_last_result(pattern, h2h_list)
        if result:
            if function:
                function(template.format(
                    team=team_name.replace("Last matches:", ""),
                    pattern=pattern.replace(":away", "").replace(":home", ""),
                    place=place
                ))


    def h2h_search_last_result(self, pattern, team="", function:Callable=None):
        h2h_list: List[Ih2h] = [Ih2h(**x) for x in self if x['place']]
        _team = {}
        for x in h2h_list:
            _team[x.match_type] = None
        team_names = [x for x in _team.keys()]

        if team == "home":
            self.get_result_h2h(team_names[0], pattern, h2h_list, function)
        elif team == "away":
            self.get_result_h2h(team_names[1], pattern, h2h_list, function)
        else:
            self.get_result_h2h(team_names[0], pattern, h2h_list, function)
            self.get_result_h2h(team_names[1], pattern, h2h_list, function)


    def _h2h_search_last_result(self, pattern: str, h2h_list:List[Ih2h]):
        pattern_list = pattern.split(":")[0].split()
        quantity = len(pattern_list)
        if quantity > len(h2h_list):
            # Матчей меньше чем паттернов
            return
        i = 0
        for e, pat in enumerate(pattern_list):

            if h2h_list[e].win_draw_lose(pattern_list[e]):
                i += 1
            else:
                return False

            if i == quantity:
                return True

