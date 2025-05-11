from config import db
from exceptions import NotFoundException
from structures.cities.city_resource_serializers import *
from models import City


def get_all():
    cities = City.query.all()

    return cities_serializer.dump(cities)

def get_city_by_id(id : int):
    city = City.query.filter_by(id=id).one_or_none()

    if city is None:
        raise NotFoundException(f'City with id {id} not found')

    return city_serializer.dump(city)

def create_city(request_body):
    city = city_deserializer.load(request_body)
    db.session.add(city)
    db.session.commit()

    return city_serializer.dump(city)

def update_city(id : int, request_body):
    dst = city_update_deserializer.load(request_body)

    src = City.query.filter_by(id=id).one_or_none()
    if src is None:
        raise NotFoundException(f'City with id {id} not found')

    src.name = dst.name
    db.session.commit()

    return city_serializer.dump(src)

def delete_city_by_id(id : int):
    removed_raws = City.query.filter_by(id=id).delete()

    if removed_raws == 0:
        raise NotFoundException(f'City with id {id} not found')

    db.session.commit()

    return True