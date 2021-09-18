### Описание

Получение структурированной информации по спортивным  live событиям.

Очень важно, все данные доступны в live режиме. 

Нельзя получать данные по матчам которые уже:
- сыграны
- запланированы

### Установка

1. `pip install digital-sport`

2. Для работы библиотеки нужен апи токен, который дает доступ к информации.
	

Апи токен можно получить:
    
- в телеграм боте @sport_api_bot (/help).
- на сайте [data-provider.ru](https://data-provider.ru).

#### Установить токен

```
from sport.api import FootballSport

token = "Your token"
football = FootballSport(token, debug=True)
```

#### Получить live матчи.

```
fixtures = football.live()
print(fixtures)
```

#### Получить статистику по мачту.

Необходим id матча.

```
# Статистика матча
data = football.statistics("match_id")
print(data)
```

#### Получить коеффициенты на матч

Необходим id матча.

```
data = football.odds("match_id")
print(data)
```

#### Получить последние/очные игры команд

Необходим id матча.
```
data = football.h2h("match_id")
print(data)
```

#### Прикрепить статистику к live матчам.

Для матчей у которых имеется статистика к этим объектам добавится их статистика.
Работа в многопоточном режиме.
Необходимо передать в метод список live матчей. 

```
fixtures = football.add_statistics(fixtures)
```