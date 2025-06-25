from flask import jsonify

from config import db
from airlines.flights.flight_serializer import *
from models import Flight, FlightStatus, Country
from sqlalchemy import func
from airlines.diagrams.diagram_serializer import *

def __convert_to_response_object(result) :
    return {
        'countryName' : result.country_name,
        'countryCode' : result.country_code,
        'minFlights' : result.min_flights,
        'maxFlights' : result.max_flights,
        'avgFlights' : result.avg_flights,
    }


def get_countries_flights_stats_at_status(request_body):
    print(request_body)
    dto = get_all_countries_stats_deserializer.load(request_body)
    print(dto)
    subq = (
        db.session.query(
            Airport.id.label('airport_id'),
            Airport.country_id.label('country_id'),
            func.count(Flight.id).label('flights')
        )
        .join(Country, Country.id == Airport.country_id)
        .join(Flight, Flight.arrival_airport_id == Airport.id)
        .filter(Flight.flight_status == dto.flight_status)
        .group_by(Airport.code, Airport.country_id, Flight.flight_status)
        .subquery()
    )

    query = (
        db.session.query(
            Country.name.label('country_name'),
            Country.code.label('country_code'),
            func.min(subq.c.flights).label('min_flights'),
            func.max(subq.c.flights).label('max_flights'),
            func.avg(subq.c.flights).label('avg_flights')
        )
        .join(subq, subq.c.country_id == Country.id)
        .group_by(Country.name, Country.code)
        .limit(100)
    )

    result = list(map(__convert_to_response_object, query.all()))

    return jsonify(result)