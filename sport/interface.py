from dataclasses import dataclass


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