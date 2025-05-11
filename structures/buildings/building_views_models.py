from config import db
from exceptions import NotFoundException
from building_views_models import Building

def find_all_buidlings():
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
    Building.query.filter_by(id=id).update(updated.__dict__)
    db.session.commit()

    return updated

def __update_model(src : Building, dst: Building):
    new_building = Building(
        id=src.id,
        type_building_id=src.type_building_id,
        city_id=src.city_id,
        title= dst.title if dst.title is not None else src.title,
        year= dst.year if dst.year is not None else src.year,
        height= dst.height if dst.height is not None else src.height,
    )

    return new_building