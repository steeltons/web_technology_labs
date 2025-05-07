import csv

from app import app
from config import db
from models import Country, City, TypeBuilding, Building

def fill_country_table():
    with open('data/country.csv', mode='r', encoding='windows-1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country = Country(
                name=row['name'],
            )
            db.session.add(country)
        db.session.commit()

def fill_type_building_table():
    with open('data/typeBuilding.csv', mode='r', encoding='windows-1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            type_building = TypeBuilding(
                type= row['type']
            )
            db.session.add(type_building)
        db.session.commit()

def fill_city_table():
    with open('data/city.csv', mode='r', encoding='windows-1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = City(
                name=row['name'],
                country_id=int(row['id']),
            )
            db.session.add(city)
        db.session.commit()

def fill_building_table():
    with open('data/building.csv', mode='r', encoding='windows-1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            building = Building(
                title=row['name'],
                type_building_id=int(row['id1']),
                city_id=int(row['id2']),
                year=int(row['year']),
                height=float(row['height'])
            )
            db.session.add(building)
        db.session.commit()

def init_database():
    app.app_context().push()
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    init_database()
    fill_country_table()
    fill_city_table()
    fill_type_building_table()
    fill_building_table()
