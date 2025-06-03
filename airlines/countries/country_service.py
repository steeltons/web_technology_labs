from config import db
from exceptions import NotFoundException
from airlines.countries.country_serializer import *
from models import Country, Airport, Flight
from flask import jsonify

from sqlalchemy import func

def get_all():
    countries = Country.query.all()
    return country_list_serializer.dump(countries)

def get_by_id(id):
    country = Country.query.filter_by(id=id).first()
    if country is None:
        raise NotFoundException(f'Country not found: id={id}')
    return country_serializer.dump(country)

def create(request_body):
    country = country_create_deserializer.load(request_body)
    db.session.add(country)
    db.session.commit()
    return country_serializer.dump(country)

def update(id, request_body):
    dst = country_update_deserializer.load(request_body)
    src = Country.query.filter_by(id=id).first()
    if src is None:
        raise NotFoundException(f'Country not found: id={id}')

    src.name = dst.name
    src.code = dst.code
    src.continent_id = dst.continent_id
    db.session.commit()
    return country_serializer.dump(dst)

def delete_by_id(id):
    removed_rows = Country.query.filter_by(id=id).delete()
    if removed_rows == 0:
        raise NotFoundException(f'Country not found: id={id}')
    db.session.commit()
    return True

def get_country_airport_departure_stats():

    subq = (
        db.session.query(
            Country.id.label('country_id'),
            Airport.id.label('airport_id'),
            func.count(Flight.id).label('departure_count')
        )
        .join(Airport, Airport.country_id == Country.id)
        .outerjoin(Flight, Flight.departure_airport_id == Airport.id)
        .group_by(Country.id, Airport.id)
        .subquery()
    )

    result = (
        db.session.query(
            Country.name.label('country_name'),
            func.min(subq.c.departure_count).label('min_departures_per_airport'),
            func.max(subq.c.departure_count).label('max_departures_per_airport'),
            func.avg(subq.c.departure_count).label('avg_departures_per_airport')
        )
        .join(subq, subq.c.country_id == Country.id)
        .group_by(Country.name)
        .all()
    )

    return jsonify({"countries": result})
