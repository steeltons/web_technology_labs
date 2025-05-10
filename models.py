from config import db

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)

    cities = db.relationship("City", cascade='all, delete')

    def __init__(self, name):
        self.name = name


class TypeBuilding(db.Model):
    __tablename__ = 'type_buildings'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column('type', db.String(50), nullable=False)

    buildings = db.relationship("Building", cascade='all, delete')

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"\n{self.id}. {self.type}"


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    country = db.relationship("Country", back_populates="cities")
    buildings = db.relationship("Building", cascade='all, delete')

    def __init__(self, name, country_id = None):
        self.name = name
        self.country_id = country_id


class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.String(200))
    type_building_id = db.Column(db.Integer, db.ForeignKey('type_buildings.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    year = db.Column(db.Integer)
    height = db.Column(db.Integer)

    type_building = db.relationship("TypeBuilding", back_populates="buildings")
    city = db.relationship("City", back_populates="buildings")

    def __init__(self, title, year, height, id= None, type_building_id=None, city_id=None):
        self.id = id
        self.title = title
        self.type_building_id = type_building_id
        self.city_id = city_id
        self.year = year
        self.height = height