from config import db
from exceptions import NotFoundException
from models import Building
from utils.utils import get_or_default
from sqlalchemy import update

def find_all_buildings():
    return Building.query.all()

def find_by_id(id : int):
    result = (
        Building.query
            .filter(Building.id == id)
            .one_or_none()
    )

    if result is None:
        raise NotFoundException(f'Building with id={id} not found')

    return result

def create(building: Building):
    db.session.add(building)
    db.session.commit()

    return building

def delete_by_id(id : int):
    deleted_rows = Building.query.filter_by(id=id).delete()
    if deleted_rows == 0:
        raise NotFoundException(f'Building with id={id} not found')
    db.session.commit()

    return True

def update(id : int, dst : Building):
    src = Building.query.filter_by(id=id).one_or_none()
    if src is None:
        raise NotFoundException(f'Building with id={id} not found')

    updated = __update_model(src, dst)
    update_dict = __get_update_dict_params(updated)
    print(update_dict)
    Building.query.filter_by(id=id).update(update_dict)
    db.session.commit()

    return updated

def __update_model(src : Building, dst: Building):
    new_building = Building(
        id=src.id,
        type_building_id=src.type_building_id,
        city_id=src.city_id,
        title= get_or_default(dst.title, src.title),
        year= get_or_default(dst.year, src.year),
        height= get_or_default(dst.height, src.height)
    )

    return new_building

def __get_update_dict_params(value : Building):
    return dict(
        id = value.id,
        type_building_id= value.type_building_id,
        city_id= value.city_id,
        title= value.title,
        year= value.year,
        height= value.height
    )