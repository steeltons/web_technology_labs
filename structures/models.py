from sqlalchemy.orm import aliased

from config import db
from models import Flight, Airport, Pilot, Continent, Country
from sqlalchemy import func, alias


def find_all_pilots_that_have_flights_more_than_or_equal_threshold(threshold : int):
    query = (
        db.session.query(
            Pilot.name.label('Пилот'),
            func.count(Pilot.id)
        )
        .select_from(Flight)
        .join(Pilot)
        .group_by(Pilot.name)
        .having(func.count(Pilot.id) >= threshold)
    )

    return query.statement.columns.keys(), query.all()

def find_all_flights_that_destination_in_same_country():
    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)

    subquery = (
        db.session.query(
            Country.id
        )
        .select_from(Country)
        .filter_by(Country.id == Airport.country_id)
    ).subquery()

    query = (
        db.session.query(
            Flight.id.label('Номер полёта'),
            Flight.departure_date.label('Дата полёта'),
            Flight.flight_status.label('Статус полёта'),
            departure_airport_alias.name.label('From'),
            arrival_airport_alias.name.label('To'),
        )
        .select_from(Flight)
        .join(departure_airport_alias, departure_airport_alias.id == Flight.departure_airport_id)
        .join(arrival_airport_alias, arrival_airport_alias.id == Flight.arrival_airport_id)
    )

    return query.statement.columns.keys(), query.all()