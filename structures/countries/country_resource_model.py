from exceptions import NotFoundException
from models import Country
from structures.countries.country_resource_serializer import *
from config import db

def get_all():
    countries = Country.query.all()

    return countries_resource_serializer.dump(countries)

def get_by_id(id : int) -> Country:
    country = Country.query.filter_by(id=id).one_or_none()

    if country is None:
        raise NotFoundException(f"Country with id {id} not found")

    return country_resource_serializer.dump(country)

def create(request_body_json) -> Country:
    country = country_resource_deserializer.load(request_body_json)
    db.session.add(country)
    db.session.commit()

    return country_resource_serializer.dump(country)

def update(id : int, request_body_json) -> Country:
    dst = country_resource_deserializer.load(request_body_json)
    src = Country.query.filter_by(id=id).one_or_none()

    if src is None:
        raise NotFoundException(f"Country with id {id} not found")

    src.name = dst.name
    db.session.commit()

    return country_resource_serializer.dump(src)

def delete(id : int) -> bool:
    deleted_raws = Country.query.filter_by(id=id).delete()

    if deleted_raws == 0:
        raise NotFoundException(f"Country with id {id} not found")

    db.session.commit()

    return True