from config import db
from exceptions import NotFoundException
from airlines.airports.airport_serializer import *
from models import Airport

def get_all():
    airports = Airport.query.all()
    return airport_list_serializer.dump(airports)

def get_by_id(id):
    airport = Airport.query.filter_by(id=id).first()
    if airport is None:
        raise NotFoundException(f'Airport not found: id={id}')
    return airport_serializer.dump(airport)

def create(request_body):
    airport = airport_create_deserializer.load(request_body)
    db.session.add(airport)
    db.session.commit()
    return airport_serializer.dump(airport)

def update(id, request_body):
    dst = airport_update_deserializer.load(request_body)
    src = Airport.query.filter_by(id=id).first()
    if src is None:
        raise NotFoundException(f'Airport not found: id={id}')

    src.name = dst.name
    src.code = dst.code
    src.country_id = dst.country_id
    db.session.commit()
    return airport_serializer.dump(dst)

def delete_by_id(id):
    removed_rows = Airport.query.filter_by(id=id).delete()
    if removed_rows == 0:
        raise NotFoundException(f'Airport not found: id={id}')
    db.session.commit()
    return True
