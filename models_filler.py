import csv
from datetime import datetime

from app import app
from models import *

__FILE_READ_MODE = 'r'

def __init_database():
    app.app_context().push()
    with app.app_context():
        db.drop_all()
        db.create_all()

def __add_pilot_to_dict(pilot_name_dict: dict, row):
    pilot_name = row['Pilot Name']

    if pilot_name not in pilot_name_dict:
        pilot = Pilot(name=pilot_name)
        pilot_name_dict[pilot_name] = pilot

def __add_continent(continent_name, continent_code) :
    continent = Continent(
        name= continent_name,
        code= continent_code,
    )
    db.session.add(continent)
    db.session.commit()
    return continent.id

def __add_continents(continent_code_id_dict, row):
    from_continent_code = row['From Continent Code']
    to_continent_code = row['To Continent Code']
    if from_continent_code not in continent_code_id_dict:
        continent_id = __add_continent(row['From Continent'], from_continent_code)
        continent_code_id_dict[from_continent_code] = continent_id
    if to_continent_code not in continent_code_id_dict:
        continent_id = __add_continent(row['To Continent'], to_continent_code)
        continent_code_id_dict[to_continent_code] = continent_id

def __add_country(country_name, country_code, continent_id):
    country = Country(
        name= country_name,
        code= country_code,
        continent_id= continent_id,
    )
    db.session.add(country)
    db.session.commit()
    return country.id

def __add_countries(country_code_id_dict, continent_code_id_dict, row):
    from_country_code = row['From Country Code']
    to_country_code = row['To Country Code']
    if from_country_code not in country_code_id_dict:
        country_id = __add_country(row['From Country'], from_country_code, continent_code_id_dict[row['From Continent Code']])
        country_code_id_dict[from_country_code] = country_id

    if to_country_code not in country_code_id_dict:
        country_id = __add_country(row['To Country'], to_country_code, continent_code_id_dict[row['To Continent Code']])
        country_code_id_dict[to_country_code] = country_id

def __add_airport(airport_name, airport_code, country_id):
    airport = Airport(
        name= airport_name,
        code= airport_code,
        country_id= country_id,
    )
    db.session.add(airport)
    db.session.commit()
    return airport.id

def __add_airports(airport_code_id_dict, country_code_id_dict, row):
    from_airport_code = row['From Airport Code']
    to_airport_code = row['To Airport Code']
    if from_airport_code not in airport_code_id_dict:
        airport_id = __add_airport(row['From Airport Name'], from_airport_code, country_code_id_dict[row['From Country Code']])
        airport_code_id_dict[from_airport_code] = airport_id

    if to_airport_code not in airport_code_id_dict:
        airport_id = __add_airport(row['To Airport Name'], to_airport_code, country_code_id_dict[row['To Country Code']])
        airport_code_id_dict[to_airport_code] = airport_id

def __add_pilot(pilot_name_id_dict, row):
    pilot_name = row['Pilot']
    pilot = Pilot(
        name= pilot_name,
    )
    db.session.add(pilot)
    db.session.commit()
    pilot_name_id_dict[pilot_name] = pilot.id

def __add_flight_info(airport_code_id_dict, pilot_name_id_dict, row):
    from_airport_id = airport_code_id_dict[row['From Airport Code']]
    to_airport_id = airport_code_id_dict[row['To Airport Code']]
    pilot_id = pilot_name_id_dict[row['Pilot']]
    departure_date = datetime.strptime(row['Departure Date'].replace('/', '-'), '%m-%d-%Y')
    flight_status = FlightStatus.find_by_column_value(row['Flight Status'])

    flight = Flight(
        departure_date= departure_date,
        pilot_id= pilot_id,
        flight_status = flight_status,
        departure_airport_id= from_airport_id,
        arrival_airport_id= to_airport_id,
    )
    db.session.add(flight)
    db.session.commit()
    return flight.id

if __name__ == '__main__':
    __init_database()
    continent_code_id_dict = dict()
    country_code_id_dict = dict()
    airport_code_id_dict = dict()
    pilot_name_id_dict = dict()

    with open('data/airline_dataset.csv', __FILE_READ_MODE) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            __add_continents(continent_code_id_dict, row)
            __add_countries(country_code_id_dict, continent_code_id_dict, row)
            __add_airports(airport_code_id_dict, country_code_id_dict, row)
            __add_pilot(pilot_name_id_dict, row)
            __add_flight_info(airport_code_id_dict, pilot_name_id_dict, row)

    ii = 43