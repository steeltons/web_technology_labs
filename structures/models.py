from sqlalchemy.orm import aliased

from config import db
from models import Flight, Airport, Pilot, Continent, Country
from sqlalchemy import func, alias, desc, distinct


def find_all_flights_with_airports_and_countries():
    departure_airport = aliased(Airport)
    arrival_airport = aliased(Airport)
    departure_country = aliased(Country)
    arrival_country = aliased(Country)

    query = (
        db.session.query(
            Flight.id,
            Flight.departure_date.label("Дата отлёта"),
            Pilot.name.label("Пилот"),
            departure_airport.name.label("Пункт отправления"),
            departure_country.name.label("Страна отправления"),
            arrival_airport.name.label("Пункт прибытия"),
            arrival_country.name.label("Страна прибытия"),
        )
        .join(Pilot, Flight.pilot)
        .join(departure_airport, Flight.departure_airport_id == departure_airport.id)
        .join(departure_country, departure_airport.country_id == departure_country.id)
        .join(arrival_airport, Flight.arrival_airport_id == arrival_airport.id)
        .join(arrival_country, arrival_airport.country_id == arrival_country.id)
        .order_by(desc(Flight.departure_date))
        .limit(100)
    )

    return query.statement.columns.keys(), query.all()

def find_all_pilots_departure_arrive_continent_same():
    departure_airport = aliased(Airport)
    arrival_airport = aliased(Airport)
    departure_country = aliased(Country)
    arrival_country = aliased(Country)
    departure_continent = aliased(Continent)
    arrival_continent = aliased(Continent)

    query = (
        db.session.query(
            Flight.id,
            Pilot.name.label("Пилот"),
            departure_country.name.label("Улетает из страны"),
            departure_continent.name.label("Улетает из континента"),
            arrival_country.name.label("Летит в страну"),
            arrival_continent.name.label("Прилетает на континент"),
        )
        .join(Pilot, Flight.pilot)
        .join(departure_airport, Flight.departure_airport_id == departure_airport.id)
        .join(departure_country, departure_airport.country_id == departure_country.id)
        .join(departure_continent, departure_country.continent_id == departure_continent.id)
        .join(arrival_airport, Flight.arrival_airport_id == arrival_airport.id)
        .join(arrival_country, arrival_airport.country_id == arrival_country.id)
        .join(arrival_continent, arrival_country.continent_id == arrival_continent.id)
        .filter(arrival_country.id == departure_country.id)
        .order_by(Pilot.name)
        .limit(100)
    )
    return query.statement.columns.keys(), query.all()

def find_continent_stats():
    """
    Возвращает список кортежей:
      (continent_name, countries_count, airports_count, departures_count)
    отсортированных по departures_count DESC, затем по continent_name.
    """
    query = (
        db.session.query(
            Continent.name.label('Название континента'),
            Continent.code.label('Код континента'),
            func.count(distinct(Country.id)).label('Число стран, в которые были полёты'),
            func.count(distinct(Airport.id)).label('Число аэропортов, в которые были полёты'),
            func.count(Flight.id).label('Число полётов'),
        )
        .join(Country, Country.continent_id == Continent.id)
        .join(Airport, Airport.country_id    == Country.id)
        .join(Flight, Flight.departure_airport_id == Airport.id)
        .group_by(Continent.name)
        .order_by(desc('Число полётов'), Continent.name)
    )

    return query.statement.columns.keys(), query.all()

def find_all_countries_arrival_greater_than_avg():
    airport_flights = (
        db.session.query(
            func.count(Flight.id).label('flight_count'),
        )
        .select_from(Country)
        .join(Airport, Country.id == Airport.country_id)
        .join(Flight, Flight.arrival_airport_id == Airport.id)
        .group_by(Country.id)
        .subquery()
    )
    avg_country_flights = (
        db.session.query(
            func.round(
                func.avg(airport_flights.c.flight_count),
                0
            ),
        )
        .select_from(airport_flights)
        .scalar_subquery()
    )

    query = (
        db.session.query(
            Country.code.label("Код страны"),
            Country.name.label("Страна"),
            func.count(Flight.id).label('Число вылетов'),
            avg_country_flights.label("Среднее число вылетов из стран")
        )
        .select_from(Country)
        .join(Airport, Country.id == Airport.country_id)
        .join(Flight, Flight.arrival_airport_id == Airport.id)
        .group_by(Country.code, Country.name)
        .having(func.count(Flight.id) > avg_country_flights)
        .order_by(desc('Число вылетов'))
    )

    return query.statement.columns.keys(), query.all()

def find_all_min_max_avg_flight_airports():
    query = (
            db.session.query(
                Airport.name,
                func.count(Flight.id).label("Число вылетов"),
                func.min(Flight.departure_date).label("Дата первого вылета"),
                func.max(Flight.departure_date).label("Дата последнего вылета"),
            )
            .outerjoin(Flight, Airport.id == Flight.departure_airport_id)
            .group_by(Airport.id)
            .order_by(desc("Число вылетов"))
        .limit(100)
    )

    return query.statement.columns.keys(), query.all()
