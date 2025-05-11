import uuid

from app import app, api
from structures.type_buildings.type_buidling_resource_model import *

from flask import request
from flask_restful import Resource
from http import HTTPStatus

class TypeBuildingResource(Resource):
    def get(self, id):
        app.logger.debug(f'START TypeBuildingResource::get id={id}')
        result = get_by_id(id)
        app.logger.debug(f'END TypeBuildingResource::get id={id}')
        return result, HTTPStatus.OK

    def put(self, id):
        request_body = request.get_json()
        app.logger.info(f'START TypeBuildingResource::put id={id}, request_body={request_body}')
        result = update(id, request_body)
        app.logger.info(f'END TypeBuildingResource::put id={id}, result={result}')
        return result, HTTPStatus.OK

    def delete(self, id):
        app.logger.info(f'START TypeBuildingResource::delete id={id}')
        delete_by_id(id)
        app.logger.info(f'END TypeBuildingResource::delete id={id}')
        return "", HTTPStatus.NO_CONTENT

class TypeBuildingListResource(Resource):
    def get(self):
        request_id = str(uuid.uuid4())
        app.logger.debug(f'START TypeBuildingListResource::get request_id={request_id}')
        result = get_all()
        app.logger.debug(f'END TypeBuildingListResource::get request_id={request_id}, type_buildings_count={len(result)}')
        return result, HTTPStatus.OK

    def post(self):
        request_body = request.get_json()
        request_id = str(uuid.uuid4())
        app.logger.info(f'START TypeBuildingListResource::post request_id={request_id}, request_body={request_body}')
        result = create(request_body)
        app.logger.info(f'END TypeBuildingListResource::post request_id={request_id}, result={result}')
        return result, HTTPStatus.CREATED

api.add_resource(TypeBuildingResource, '/structures/api/v1/type-buildings/<int:id>')
api.add_resource(TypeBuildingListResource, '/structures/api/v1/type-buildings')