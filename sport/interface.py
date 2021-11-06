from dataclasses import dataclass
import re


class IBase:

    def to_dict(self):
        return self.__dict__


@dataclass
class Ih2h(IBase):
    match_id: str
    league: str
    country: str
    start_time: int
    home_team_name: str
    away_team_name: str
    home_team_goals: int
    away_team_goals: int
    match_type: str
    snapshot_time: int
    result: str
    place: str

    def win_draw_lose(self, pattern: str) -> bool:
        return pattern == self.result

    def total(self,):
        pass


@dataclass
class FootballMatch(IBase):
    match_id: str
    start_time: int
    home_team: str
    away_team: str
    league: str
    country: str
    home_goals: int
    away_goals: int
    elapsed_time: int
    extra_time: str
    match_status: str
    home_goals_before45: int
    away_goals_before45: int
    statistics: str


@dataclass
class IStatistics(IBase):
    match_id: str
    snapshot_time: int
    match_period: str
    home_value: str
    name: str
    away_value: str

    def get_name(self, name):
        return self.name == name

    def get_period(self, name):
        return self.match_period == name

    def get_expression(self, pattern):
        """
        Patterns:
            home>10
            home=50
            away<50
            <10

        """
        home_value = float(self.home_value.replace("%", "").strip())
        away_value = float(self.away_value.replace("%", "").strip())
        # =============
        patterns = re.search(r"^(.*?)(>|=|<)(.*)$", pattern)
        groups = patterns.groups()
        groups = tuple(filter(lambda x: x, groups))

        if len(groups) == 3:
            target, mark, value = groups
            team_value = home_value
            if target == "away":
                team_value = away_value
            template = "{team_value} {mark} {val}"
            return eval(template.format(team_value=team_value,
                                        mark=mark.replace("=", "=="), val=float(value.strip())))
        elif len(groups) == 2:
            mark, value = groups
            mark = mark.replace("=", "==")
            template01 = f"{home_value} {mark} {float(value.strip())}"
            template02 = f"{away_value} {mark} {float(value.strip())}"
            return eval(template01) or eval(template02)
        else:
            return False

    def __gt__(self, other):
        home_val = int(self.home_value.replace("%", ""))
        away_val = int(self.away_value.replace("%", ""))

        other_home_val = int(other.home_value.replace("%", ""))
        other_away_val = int(other.away_value.replace("%", ""))

        # if home_val > away_val:
        #     return home_val > other_home_val
        # else:
        #     return away_val > other_away_val
        return home_val + away_val > other_home_val + other_away_val
        # if self.home_value
        # return self.away_value > other.y