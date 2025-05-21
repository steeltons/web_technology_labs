from http import HTTPStatus
from flask import make_response, request
from app import app, auth
from structures.buildings.building_views_models import find_all_buildings, find_by_id, create, delete_by_id, update
from structures.buildings.building_views_serializers import building_schema, building_schemas, building_deserializer, building_update_deserializer

_DELETE_SUCCESS_RESPONSE = {"success": True}

@app.route('/structures/api/v1/buildings', methods=['GET'])
@auth.login_required
def get_all_buildings():
    buildings = find_all_buildings()

    return make_response(building_schemas.dump(buildings), HTTPStatus.OK)

@app.route('/structures/api/v1/buildings/<id>', methods=['GET'])
# @auth.login_required
def get_building(id : int):
    buidling = find_by_id(id)

    return make_response(building_schema.dump(buidling), HTTPStatus.OK)

@app.route('/structures/api/v1/buildings', methods=['POST'])
# @auth.login_required
def create_building():
    body = request.get_json()
    deserialized = building_deserializer.load(body)

    persisted = create(deserialized)
    return make_response(building_schema.dump(persisted), HTTPStatus.CREATED)

@app.route('/structures/api/v1/buildings/<id>', methods=['PUT'])
@auth.login_required
def update_building(id : int):
    model = building_update_deserializer.load(request.get_json())

    updated = update(id, model)
    return make_response(building_schema.dump(updated), HTTPStatus.OK)

    raise NotImplementedError()

@app.route('/structures/api/v1/buildings/<id>', methods=['DELETE'])
@auth.login_required
def delete_building(id : int):
    delete_by_id(id)

    return make_response(_DELETE_SUCCESS_RESPONSE, 200)