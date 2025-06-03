from config import db
from exceptions import NotFoundException
from airlines.pilots.pilot_serializer import *
from models import Pilot

def get_all():
    pilots = Pilot.query.all()
    return pilot_list_serializer.dump(pilots)

def get_by_id(id):
    pilot = Pilot.query.filter_by(id=id).first()
    if pilot is None:
        raise NotFoundException(f'Pilot not found: id={id}')
    return pilot_serializer.dump(pilot)

def create(request_body):
    pilot = pilot_create_deserializer.load(request_body)
    db.session.add(pilot)
    db.session.commit()
    return pilot_serializer.dump(pilot)

def update(id, request_body):
    dst = pilot_update_deserializer.load(request_body)
    src = Pilot.query.filter_by(id=id).first()
    if src is None:
        raise NotFoundException(f'Pilot not found: id={id}')

    src.name = dst.name
    db.session.commit()
    return pilot_serializer.dump(dst)

def delete_by_id(id):
    removed_rows = Pilot.query.filter_by(id=id).delete()
    if removed_rows == 0:
        raise NotFoundException(f'Pilot not found: id={id}')
    db.session.commit()
    return True
