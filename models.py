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

class FlightStatus(enum.Enum):

    UNKNOWN = 0, 'UNKNOWN'
    ON_TIME = 1, 'В пути',
    CANCELLED = 2, 'Отменён',
    DELAYED = 3, 'Завершён',

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _, display_name):
        self.display_name = display_name

    @staticmethod
    def find_by_column_value(value):
        for status in FlightStatus:
            if value == status.column_value:
                return status
        raise Exception(f"FlightStatus was'n found: value={value}")

class Continent(db.Model):
    __tablename__ = 'continents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100))

    countries = db.relationship('Country', back_populates='continent', cascade='all, delete', lazy='dynamic')

    def __init__(self, name, code, id=None):
        self.id = id
        self.name = name
        self.code = code

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    continent_id = db.Column(db.Integer, db.ForeignKey('continents.id'))

    continent = db.relationship("Continent", back_populates="countries")
    airports = db.relationship("Airport", cascade='all, delete', lazy='dynamic')
    images = db.relationship("CountryImage", cascade="all, delete", back_populates="country")

    def __init__(self, name, code, continent_id=None, id=None):
        self.id = id
        self.name = name
        self.code = code
        self.continent_id = continent_id

class Airport(db.Model):
    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    country = db.relationship("Country", back_populates="airports")

    departures = db.relationship('Flight', foreign_keys='Flight.departure_airport_id', back_populates='departure_airport')
    arrivals = db.relationship('Flight', foreign_keys='Flight.arrival_airport_id', back_populates='arrival_airport')

    def __init__(self, name, code, country_id=None, id=None):
        self.id = id
        self.name = name
        self.code = code
        self.country_id = country_id

class Pilot(db.Model):
    __tablename__ = 'pilots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    flights = db.relationship('Flight', back_populates='pilot')

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    departure_date = db.Column(db.Date)
    flight_status = db.Column(Enum(FlightStatus))

    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'))

    pilot = db.relationship("Pilot", back_populates="flights")
    departure_airport = db.relationship("Airport", foreign_keys=[departure_airport_id], back_populates="departures")
    arrival_airport = db.relationship("Airport", foreign_keys=[arrival_airport_id], back_populates="arrivals")

    def __init__(self, departure_date, flight_status=FlightStatus.UNKNOWN, departure_airport_id=None, arrival_airport_id=None, pilot_id=None, id=None):
        self.id = id
        self.departure_date = departure_date
        self.flight_status = flight_status
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.pilot_id = pilot_id

class CountryImage(db.Model):
    __tablename__ = 'country_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    country = db.relationship("Country", back_populates="images")