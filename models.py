import enum

from config import db
from sqlalchemy import Enum

class ContinentCode(enum.Enum):

    UNKNOWN = 0
    AS = 1
    EU = 2
    NA = 3
    OC = 4
    AF = 5
    SA = 6

class Continent(db.Model):

    __tablename__ = 'continents'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    code = db.Column('code', db.String(100))

    countries = db.relationship('Country', cascade='all, delete', lazy='dynamic')

    def __init__(self, name, code):
        self.name = name
        self.code = code

class Country(db.Model):

    __tablename__ = 'countries'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    code = db.Column('code', db.String(100))
    continent_id = db.Column('continent_id', db.Integer, db.ForeignKey('continents.id'))

    continent = db.relationship("Continent", back_populates="countries")
    airports = db.relationship("Airport", cascade='all, delete', lazy='dynamic')

    def __init__(self, name, code, continent_id= None):
        self.name = name
        self.code = code
        self.continent_id = continent_id

class Airport(db.Model):

    __tablename__ = 'airports'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    code = db.Column('code', db.String(100))
    country_id = db.Column('country_id', db.Integer, db.ForeignKey('countries.id'))

    country = db.relationship("Country", back_populates="airports")

    def __init__(self, name, code, country_id= None):
        self.name = name
        self.code = code
        self.country_id = country_id

class Pilot(db.Model):

    __tablename__ = 'pilots'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))

    flights = db.relationship('Flight', back_populates='pilot')

    def __init__(self, name):
        self.name = name

class FlightStatus(enum.Enum):

    UNKNOWN = 0, 'UNKNOWN'
    ON_TIME = 1, 'On Time',
    CANCELLED = 2, 'Cancelled',
    DELAYED = 3, 'Delayed',

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _, column_value):
        self.column_value = column_value

    @staticmethod
    def find_by_column_value(value):
        for status in FlightStatus:
            if value == status.column_value:
                return status
        raise Exception(f"FlightStatus was'n found: value={value}")

class Flight(db.Model):

    __tablename__ = 'flights'

    id = db.Column('id', db.Integer, primary_key=True)
    departure_date = db.Column('departure_date', db.Date)
    flight_status = db.Column('flight_status', Enum(FlightStatus))
    departure_airport_id = db.Column('departure_airport_id', db.Integer, db.ForeignKey('airports.id'))
    arrival_airport_id = db.Column('arrival_airport_id', db.Integer, db.ForeignKey('airports.id'))
    pilot_id = db.Column('pilot_id', db.Integer, db.ForeignKey('pilots.id'))

    # departure_airport = db.relationship("Airport")
    # arrival_airport = db.relationship("Airport")
    pilot = db.relationship("Pilot", back_populates="flights")

    def __init__(self, departure_date, flight_status= FlightStatus.UNKNOWN, departure_airport_id=None, arrival_airport_id=None, pilot_id=None):
        self.departure_date = departure_date
        self.flight_status = flight_status
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.pilot_id = pilot_id