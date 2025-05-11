import uuid

from app import app, api
from structures.countries.country_resource_model import *

from flask import request
from flask_restful import Resource
from http import HTTPStatus

class CountryResource(Resource):
    def get(self, id):
        app.logger.debug(f'START CountryResource::get id={id}')
        result = get_by_id(id)
        app.logger.debug(f'END CountryResource::get id={id}, result={result}')
        return result, HTTPStatus.OK

    def put(self, id):
        request_data = request.get_json()
        app.logger.info(f'START CountryResource::put id={id}, request_data={request_data}')
        result = update(id, request_data)
        app.logger.info(f'END CountryResource::put id={id}, result={result}')
        return result, HTTPStatus.OK

    def delete(self, id):
        app.logger.info(f'START CountryResource::delete id={id}')
        delete(id)
        app.logger.info(f'END CountryResource::delete id={id}')
        return "", HTTPStatus.NO_CONTENT

class CountryListResource(Resource):
    def get(self):
        request_id = str(uuid.uuid4())
        app.logger.debug(f'START CountryListResource::get request_id={request_id}')
        result = get_all()
        app.logger.debug(f'END CountryListResource::get request_id={request_id}, country_count={len(result)}')
        return result, HTTPStatus.OK

    def post(self):
        request_data = request.get_json()
        request_id = str(uuid.uuid4())
        app.logger.info(f'START CountryListResource::post request_id={request_id}, request_data={request_data}')
        result = create(request_data)
        app.logger.info(f'END CountryListResource::post request_id={request_id}, result={result}')
        return result, HTTPStatus.CREATED

api.add_resource(CountryResource, '/structures/api/v1/countries/<int:id>')
api.add_resource(CountryListResource, '/structures/api/v1/countries')