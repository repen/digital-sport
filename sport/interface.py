"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import re
from dataclasses import dataclass, asdict


@dataclass
class IBase:

    def to_dict(self):
        return asdict(self)


@dataclass
class Ih2h(IBase):
    match_id: str               # Идентификатор матча
    away_team_goals: int        # Количество голов команды гостей (например, 2)
    away_team_name: str         # Название команды гостей (например, "Paris SG")
    country: str                # Страна, в которой проходил матч (например, "World")
    home_team_goals: int        # Количество голов домашней команды (например, 3)
    home_team_name: str         # Название домашней команды (например, "Cerezo Osaka")
    league: str                 # Название лиги или турнира, в котором проходил матч (например, "Club Friendly")
    match_type: str             # Тип матча (например, "Last matches: Paris SG")
    place: str                  # Место проведения матча (например, "" - пустая строка, если место не указано)
    result: str                 # Результат матча (например, "" - пустая строка, если результат не указан)
    snapshot_time: int          # Время снимка данных в формате UNIX timestamp
    start_time: int             # Время начала матча в формате UNIX timestamp

    def win_draw_lose(self, pattern: str) -> bool:
        return pattern == self.result

    def total(self,):
        pass


@dataclass
class IFootballMatch(IBase):
    match_id: str                 # Идентификатор матча
    away_goals: int               # Количество голов у команды гостей (например, 1)
    away_goals_before45: int      # Количество голов у команды гостей до 45-й минуты матча (например, 1)
    away_team: str                # Название команды гостей (например, "Flamengo RJ U19")
    country: str                  # Страна, в которой проходит матч (например, "WORLD")
    elapsed_time: int             # Прошедшее время матча в минутах (например, 82)
    extra_time: str               # Время дополнительного времени (например, "" - пустая строка, если нет дополнительного времени)
    home_goals: int               # Количество голов у домашней команды (например, 0)
    home_goals_before45: int      # Количество голов у домашней команды до 45-й минуты матча (например, 0)
    home_team: str                # Название домашней команды (например, "Sparta Prague U19")
    league: str                   # Название лиги или турнира, в котором проходит матч (например, "CEE Cup - Play Offs")
    match_status: str             # Статус матча
    statistics: str               # Идентификатор статистики матча (например, "r9k7lFjG")
    start_time: int               # Время начала матча в формате UNIX timestamp


@dataclass
class IStatistics(IBase):
    match_id: str           # Идентификатор матча
    snapshot_time: int      # Время снимка данных в формате UNIX timestamp
    home_value: str         # Значение статистики для домашней команды (например, "63%")
    away_value: str         # Значение статистики мячом для гостевой команды (например, "37%")
    match_period: str       # Период матча, к которому относится статистика (например, "Match")
    name: str               # Название статистики (например, "Ball Possession")


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


@dataclass
class IMarketData(IBase):
    bookmaker: str          # Имя букмекера, предоставившего данные
    market_name: str        # Название рынка ставок (например, "1Х2" - результат матча)
    market_type: str        # Тип рынка (например, "1" - одиночная ставка)
    match_id: str           # Идентификатор матча
    new_value: str          # Новое значение коэффициента (например, после обновления)
    old_value: str          # Старое значение коэффициента (например, до обновления)
    period: str             # Период события, к которому относится рынок (например, "Осн. время" - основное время матча)
    snapshot_time: int      # Время снимка данных в формате UNIX timestamp
