from config import db
from exceptions import NotFoundException
from airlines.flights.flight_serializer import *
from models import Flight, FlightStatus

def get_all():
    flights = Flight.query.all()
    return flight_list_serializer.dump(flights)

def get_by_id(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        raise NotFoundException(f'Flight not found: id={id}')
    return flight_serializer.dump(flight)

def create(request_body):
    flight = flight_create_deserializer.load(request_body)

    db.session.add(flight)
    db.session.commit()
    return flight_serializer.dump(flight)

def update(id, request_body):
    dst = flight_update_deserializer.load(request_body)
    src = Flight.query.filter_by(id=id).first()
    if src is None:
        raise NotFoundException(f'Flight not found: id={id}')

    src.departure_date = dst.departure_date
    src.flight_status = dst.flight_status
    src.departure_airport_id = dst.departure_airport_id
    src.arrival_airport_id = dst.arrival_airport_id
    src.pilot_id = dst.pilot_id
    db.session.commit()
    return flight_serializer.dump(dst)

def delete_by_id(id):
    removed_rows = Flight.query.filter_by(id=id).delete()
    if removed_rows == 0:
        raise NotFoundException(f'Flight not found: id={id}')
    db.session.commit()
    return True
