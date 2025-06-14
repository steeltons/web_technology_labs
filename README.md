# Практическая работа №1

## Предметная область - перелёты

### Составленные запросы

1. Получение информации по всем полётам с присоединением аэропортов и стран
2. Получение всех пилотов, кто вылетал и прилетал в ту же самую страну
3. Статистика по континиенту (число стран, в которые происходил перелёт, число аэропортов и кол-во перелётов)
4. Получение всех стран, число прилётов в которые больше, чем среднее число прилётов по всем странам
5. Статистика по аэропорту (число вылетов, мин и макс дата вылета)

Примеры запросов:

Первый:
```
SELECT
  f.id,
  f.departure_date        AS "Дата отлёта",
  p.name                  AS "Пилот",
  da.name                 AS "Пункт отправления",
  dc.name                 AS "Страна отправления",
  aa.name                 AS "Пункт прибытия",
  ac.name                 AS "Страна прибытия"
FROM flights AS f
  JOIN pilots     AS p  ON f.pilot_id               = p.id
  JOIN airports   AS da ON f.departure_airport_id   = da.id
  JOIN countries  AS dc ON da.country_id            = dc.id
  JOIN airports   AS aa ON f.arrival_airport_id     = aa.id
  JOIN countries  AS ac ON aa.country_id            = ac.id
ORDER BY
  f.departure_date DESC
LIMIT 100;
```

Второй:
```
SELECT
  f.id,
  p.name                    AS "Пилот",
  dc.name                   AS "Улетает из страны",
  dcont.name                AS "Улетает из континента",
  ac.name                   AS "Летит в страну",
  acont.name                AS "Прилетает на континент"
FROM flights AS f
  JOIN pilots     AS p     ON f.pilot_id               = p.id
  JOIN airports   AS da    ON f.departure_airport_id   = da.id
  JOIN countries  AS dc    ON da.country_id            = dc.id
  JOIN continents AS dcont ON dc.continent_id          = dcont.id
  JOIN airports   AS aa    ON f.arrival_airport_id     = aa.id
  JOIN countries  AS ac    ON aa.country_id            = ac.id
  JOIN continents AS acont ON ac.continent_id          = acont.id
WHERE
  dc.id = ac.id
ORDER BY
  p.name
LIMIT 100;
```

Третий:
```
SELECT
  cont.name                   AS "Название континента",
  cont.code                   AS "Код континента"
  COUNT(DISTINCT c.id)        AS "Число стран, в которые были полёты",
  COUNT(DISTINCT a.id)        AS "Число аэропортов, в которые были полёты",
  COUNT(f_dep.id)             AS "Число полётов"
FROM continents cont
  JOIN countries c ON c.continent_id           = cont.id
  JOIN airports  a ON a.country_id             = c.id
  JOIN flights   f_dep ON f_dep.departure_airport_id = a.id
GROUP BY
  cont.name
ORDER BY
  departures_count DESC,
  cont.name;
```
Четвёртый:
```
-- вычисляем среднее число прилётов на страну
WITH airport_flights AS (
  SELECT
    c.id           AS country_id,
    COUNT(f.id)    AS flight_count
  FROM countries AS c
    JOIN airports AS a ON a.country_id = c.id
    JOIN flights  AS f ON f.arrival_airport_id = a.id
  GROUP BY
    c.id
),
avg_f AS (
  SELECT ROUND(AVG(af.flight_count), 0) AS avg_flights
  FROM airport_flights AS af
)
SELECT
  c.code                                      AS "Код страны",
  c.name                                      AS "Страна",
  COUNT(f.id)                                 AS "Число вылетов",
  (SELECT avg_flights FROM avg_f)             AS "Среднее число вылетов из стран"
FROM countries AS c
  JOIN airports AS a ON a.country_id = c.id
  JOIN flights  AS f ON f.arrival_airport_id = a.id
GROUP BY
  c.code, c.name
HAVING
  COUNT(f.id) > (SELECT avg_flights FROM avg_f)
ORDER BY
  "Число вылетов" DESC;
```

Пятый:
```
SELECT
  a.name                   AS "Аэропорт",
  COUNT(f.id)              AS "Число вылетов",
  MIN(f.departure_date)    AS "Дата первого вылета",
  MAX(f.departure_date)    AS "Дата последнего вылета"
FROM airports AS a
  LEFT JOIN flights AS f   ON f.departure_airport_id = a.id
GROUP BY
  a.id, a.name
ORDER BY
  "Число вылетов" DESC
LIMIT 100;
```

### Описание таблиц:

Continents

| Поле   | Тип            | Описание                                          |
| ------ | -------------- | ------------------------------------------------- |
| `id`   | `INTEGER`      | PK, уникальный идентификатор континента           |
| `name` | `VARCHAR(100)` | Название континента                               |
| `code` | `VARCHAR(100)` | Код континента (значения из `ContinentCode` enum) |


Countries

| Поле           | Тип            | Описание                                               |
| -------------- | -------------- | ------------------------------------------------------ |
| `id`           | `INTEGER`      | PK, уникальный идентификатор страны                    |
| `name`         | `VARCHAR(100)` | Название страны                                        |
| `code`         | `VARCHAR(100)` | Код страны                                             |
| `continent_id` | `INTEGER`      | FK → `continents.id`, ссылка на родительский континент |


Airports

| Поле         | Тип            | Описание                               |
| ------------ | -------------- | -------------------------------------- |
| `id`         | `INTEGER`      | PK, уникальный идентификатор аэропорта |
| `name`       | `VARCHAR(100)` | Название аэропорта                     |
| `code`       | `VARCHAR(100)` | Код аэропорта (IATA/ICAO)              |
| `country_id` | `INTEGER`      | FK → `countries.id`, ссылка на страну  |


Pilots

| Поле   | Тип            | Описание                            |
| ------ | -------------- | ----------------------------------- |
| `id`   | `INTEGER`      | PK, уникальный идентификатор пилота |
| `name` | `VARCHAR(100)` | ФИО (или имя) пилота                |

Flights

| Поле                   | Тип                  | Описание                                                    |
| ---------------------- | -------------------- | ----------------------------------------------------------- |
| `id`                   | `INTEGER`            | PK, уникальный идентификатор рейса                          |
| `departure_date`       | `DATE`               | Дата (и время, если нужно) вылета                           |
| `flight_status`        | `ENUM(FlightStatus)` | Статус рейса (`UNKNOWN`, `On Time`, `Cancelled`, `Delayed`) |
| `departure_airport_id` | `INTEGER`            | FK → `airports.id`, аэропорт вылета                         |
| `arrival_airport_id`   | `INTEGER`            | FK → `airports.id`, аэропорт прилёта                        |
| `pilot_id`             | `INTEGER`            | FK → `pilots.id`, пилот, управляющий рейсом                 |

### Запуск проекта:

1. Запустить скрипт start_flask.sh -- если UNIX
2. Если не UNIX, то запучтить start_flask.bat
3. Перейти по ссылке http://localhost:5000/ -- открется страница со всеми запросами