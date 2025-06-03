from uuid import uuid4

from http import HTTPStatus
from flask import make_response, request
from app import app
from airlines.countries.country_service import *

__REQUEST_MAPPING_URL = '/api/v1/countries'

@app.route(__REQUEST_MAPPING_URL, methods=['GET'])
def get_all_countries():
    request_id = uuid4()
    app.logger.debug(f'START country_view.get_all_countries request_id={str(request_id)}')
    result = get_all()
    app.logger.debug(f'END country_view.get_all_countries request_id={str(request_id)}, count={len(result)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['GET'])
def get_country_by_id(id):
    app.logger.debug(f'START country_view.get_country_by_id id={str(id)}')
    result = get_by_id(id)
    app.logger.debug(f'END country_view.get_country_by_id id={str(id)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL, methods=['POST'])
def create_new_country():
    request_id = uuid4()
    request_data = request.get_json()
    app.logger.info(f"START country_view.create_new_country request_id={str(request_id)}, request_body={request_data}")
    result = create(request_data)
    app.logger.info(f'END country_view.create_new_country request_id={str(request_id)}, result={result}')
    return make_response(result, HTTPStatus.CREATED)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['PUT'])
def update_existing_country(id):
    request_data = request.get_json()
    app.logger.info(f"START country_view.update_existing_country id={id}, update_body={request_data}")
    result = update(id, request_data)
    app.logger.info(f'END country_view.update_existing_country id={id}, result={result}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['DELETE'])
def delete_existing_country(id):
    app.logger.info(f"START country_view.delete_existing_country id={id}")
    delete_by_id(id)
    app.logger.info(f"END country_view.delete_existing_country id={id}")
    return make_response('', HTTPStatus.NO_CONTENT)


@app.route(__REQUEST_MAPPING_URL + '/stats', methods=['GET'])
def get_country_stats():
    request_id = uuid4()
    app.logger.debug(f'START country_view.get_country_stats request_id={str(request_id)}')
    result = get_country_airport_departure_stats()
    app.logger.debug(f'END country_view.get_country_stats request_id={str(request_id)}')
    return make_response(result, HTTPStatus.OK)
