from config import db
from exceptions import NotFoundException
from airlines.continents.continent_serializer import *
from models import Continent, Country, Airport, Flight
from flask import jsonify

from sqlalchemy import func


def get_all():
    continents = Continent.query.all()

    return continent_list_serializer.dump(continents)

def get_by_id(id):
    continent = Continent.query.filter_by(id=id).first()

    if continent is None:
        raise NotFoundException(f'Continent not found: id={id}')

    return continent_serializer.dump(continent)

def create(request_body):
    continent = continent_create_deserializer.load(request_body)
    db.session.add(continent)
    db.session.commit()

    return continent_serializer.dump(continent)

def update(id, request_body):
    dst = continent_update_deserializer.load(request_body)
    src = Continent.query.filter_by(id=id).first()

    if src is None:
        raise NotFoundException(f'Continent not found: id={id}')

    src.name = dst.name
    src.code = dst.code
    db.session.commit()

    return continent_serializer.dump(dst)

def delete_by_id(id):
    removed_rows = Continent.query.filter_by(id=id).delete()

    if removed_rows == 0:
        raise NotFoundException(f'Continent not found: id={id}')

    db.session.commit()
    return True

def get_continent_flights_departure_state():
    # Подзапрос: число вылетов по каждому аэропорту и континенту
    subq = (
        db.session.query(
            Continent.id.label('continent_id'),
            Airport.id.label('airport_id'),
            func.count(Flight.id).label('departure_count')
        )
        .join(Country, Country.continent_id == Continent.id)
        .join(Airport, Airport.country_id == Country.id)
        .join(Flight, Flight.departure_airport_id == Airport.id)
        .group_by(Continent.id, Airport.id)
        .subquery()
    )

    # Внешний запрос: агрегат по континентам
    result = (
        db.session.query(
            Continent.name.label('Континент'),
            Continent.code.label('Код континента'),
            func.min(subq.c.departure_count).label('Мин. вылетов'),
            func.max(subq.c.departure_count).label('Макс. вылетов'),
            func.avg(subq.c.departure_count).label('Среднее число вылетов')
        )
        .join(subq, subq.c.continent_id == Continent.id)
        .group_by(Continent.name)
        .all()
    )

    return jsonify({"continents": result})