import uuid

from app import app, api
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from structures.cities.city_resource_model import *

class CityResource(Resource):

    def get(self, id):
        app.logger.debug(f'START CityResource::get id={id}')
        result = get_city_by_id(id)
        app.logger.debug(f'END CityResource::get id={id}')
        return result, HTTPStatus.OK

    def put(self, id):
        request_data = request.get_json()
        app.logger.debug(f'START CityResource::put id={id} request_data={request_data}')
        result = update_city(id, request_data)
        app.logger.debug(f'END CityResource::put id={id} result={result}')
        return result, HTTPStatus.OK

    def delete(self, id):
        app.logger.debug(f'START CityResource::delete id={id}')
        result = delete_city_by_id(id)
        app.logger.info(f'END CityResource::delete id={id}')

        return "", HTTPStatus.NO_CONTENT

class CitiesResource(Resource):
    def get(self):
        request_id = uuid.uuid4()
        app.logger.debug(f'START CitiesResource::get request_id={str(request_id)}')
        result = get_all()
        app.logger.debug(f'END CitiesResource::get request_id={str(request_id)}, cities_count={len(result)}')

        return result, HTTPStatus.OK

    def post(self):
        request_data = request.get_json()
        app.logger.info(f'START CitiesResource::create request_data={request_data}')
        result = create_city(request_data)
        app.logger.info(f'END CitiesResource::create request_data={result}')
        return result, HTTPStatus.CREATED

api.add_resource(CityResource, '/structures/api/v1/cities/<int:id>')
api.add_resource(CitiesResource, '/structures/api/v1/cities')