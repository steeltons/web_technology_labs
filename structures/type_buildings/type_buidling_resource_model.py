from exceptions import NotFoundException
from config import db
from structures.type_buildings.type_building_resource_serializer import *

def get_by_id(id : id) -> TypeBuilding:
    type_building = TypeBuilding.query.filter_by(id=id).one_or_none()

    if type_building is None:
        raise NotFoundException(f'TypeBuilding with id={id} was not found')

    return type_building_serializer.dump(type_building)

def get_all():
    type_buildings = TypeBuilding.query.all()

    return type_buildings_serializer.dump(type_buildings)

def create(type_building_json) -> TypeBuilding:
    type_building = type_building_deserializer.load(type_building_json)
    db.session.add(type_building)
    db.session.commit()

    return type_building_serializer.dump(type_building)

def update(id : int, type_building_json) -> TypeBuilding:
    dst = type_building_deserializer.load(type_building_json)
    src = TypeBuilding.query.filter_by(id=id).one_or_none()

    if src is None:
        raise NotFoundException(f'TypeBuilding with id={id} was not found')

    src.type = dst.type
    db.session.commit()

    return type_building_serializer.dump(src)

def delete_by_id(id : int) -> bool:
    deleted_raws = TypeBuilding.query.filter_by(id=id).delete()

    if deleted_raws == 0:
        raise NotFoundException(f'TypeBuilding with id={id} was not found')

    db.session.commit()

    return True