from config import db
from models import Country, City, Building, TypeBuilding
from sqlalchemy import func, desc

def find_all_buildings():
    query = (
        db.session.query(
            Building.title.label('Здание'),
            TypeBuilding.type.label('Тип'),
            Country.name.label('Город'),
            Building.year.label('Год'),
            Building.height.label('Высота')
        )
        .select_from(Building)
        .join(TypeBuilding)
        .join(City)
        .join(Country)
        .order_by(desc(Building.height))
    )

    return [query.statement.columns.keys(), query.all()]

def find_all_type_building_with_min_max_avh_height():
    query = (
        db.session.query(
            TypeBuilding.type.label('Тип'),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .select_from(TypeBuilding)
        .join(Building, Building.type_building_id == TypeBuilding.id)
        .group_by(TypeBuilding.type)
    )

    return query.statement.columns.keys(), query.all()

def find_all_country_buildings_order_by_county_name():
    query = (
        db.session.query(
            Country.name.label('Страна'),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .select_from(Country)
        .join(City, Country.id == City.country_id)
        .join(Building, Building.city_id == City.id)
        .group_by(Country.name)
        .order_by(Country.name)
    )

    return query.statement.columns.keys(), query.all()

def find_all_building_stats_by_year_order_by_year():
    query = (
        db.session.query(
            Building.year.label("Год"),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .select_from(Building)
        .group_by(Building.year)
        .order_by(Building.year)
    )

    return query.statement.columns.keys(), query.all()

def find_all_type_buildings_stats_type_similar(type_name: str):
    query = (
        db.session.query(
            TypeBuilding.type.label('Тип здания'),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .select_from(TypeBuilding)
        .join(Building, Building.type_building_id == TypeBuilding.id)
        .filter(TypeBuilding.type.like(f'%{type_name.lower()}%'))
        .group_by(TypeBuilding.type)
        .order_by(desc('Средняя высота'))
    )

    return query.statement.columns.keys(), query.all()

def find_height_stats_for_countries_with_multiple_buildings():
    subquery = (
        db.session
        .query(Building.city_id)
        .select_from(Building)
        .group_by(Building.city_id)
        .having(func.count(Building.id) > 1)
        .subquery()
    )

    query = (
        db.session.query(
            Country.name.label('Страна'),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .select_from(Country)
        .join(City, City.country_id == Country.id)
        .join(Building, Building.city_id == City.id)
        .filter(City.id.in_(subquery))
        .group_by(Country.name)
    )

    return query.statement.columns.keys(), query.all()