from uuid import uuid4

from http import HTTPStatus
from venv import logger

from flask import make_response, request
from app import app
from airlines.continents.continent_service import *

__REQUEST_MAPPING_URL = '/api/v1/continents'

@app.route(__REQUEST_MAPPING_URL, methods=['GET'])
def get_all_continents():
    request_id = uuid4()
    app.logger.debug(f'START continent_view.get_all_continents request_id={str(request_id)}')
    result = get_all()
    app.logger.debug(f'END continent_view.get_all_continents request_id={str(request_id)}, count={len(result)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + "/<id>", methods=['GET'])
def get_continent_by_id(id):
    app.logger.debug(f'START continent_view.get_continent_by_id id={str(id)}')
    result = get_by_id(id)
    app.logger.debug(f'END continent_view.get_continent_by_id id={str(id)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL, methods=['POST'])
def create_new_continent():
    request_id = uuid4()
    request_data = request.get_json()
    app.logger.info(f"START continent_view.create_new_continent request_id={str(request_id)}, request_body={request_data}")
    result = create(request_data)
    app.logger.info(f'END continent_view.create_new_continent request_id={str(request_id)}, result={result}')
    return make_response(result, HTTPStatus.CREATED)

@app.route(__REQUEST_MAPPING_URL + "/<id>", methods=['PUT'])
def update_existing_continent(id):
    request_data = request.get_json()
    app.logger.info(f"START continent_view.update_existing_continent id={id}, update_body={request_data}")
    result = update(id, request_data)
    app.logger.info(f'END continent_view.update_existing_continent id={id}, result={result}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + "/<id>", methods=['DELETE'])
def delete_existing_continent(id):
    app.logger.info(f"START continent_view.delete_existing_continent id={id}")
    delete_by_id(id)
    app.logger.info(f"END continent_view.delete_existing_continent id={id}")
    return make_response("", HTTPStatus.NO_CONTENT)

@app.route(__REQUEST_MAPPING_URL + "/stats", methods=['GET'])
def get_continent_stats():
    request_id = uuid4()
    app.logger.debug(f'START continent_view.get_continent_stats request_id={str(request_id)}')
    result = get_continent_stats(request_id)
    app.logger.debug(f'END continent_view.get_continent_stats request_id={str(request_id)}')
    return make_response(result, HTTPStatus.OK)
