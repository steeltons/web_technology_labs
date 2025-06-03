from uuid import uuid4

from http import HTTPStatus
from flask import make_response, request
from app import app
from airlines.airports.airport_service import *

__REQUEST_MAPPING_URL = '/api/v1/airports'

@app.route(__REQUEST_MAPPING_URL, methods=['GET'])
def get_all_airports():
    request_id = uuid4()
    app.logger.debug(f'START airport_view.get_all_airports request_id={str(request_id)}')
    result = get_all()
    app.logger.debug(f'END airport_view.get_all_airports request_id={str(request_id)}, count={len(result)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['GET'])
def get_airport_by_id(id):
    app.logger.debug(f'START airport_view.get_airport_by_id id={str(id)}')
    result = get_by_id(id)
    app.logger.debug(f'END airport_view.get_airport_by_id id={str(id)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL, methods=['POST'])
def create_new_airport():
    request_id = uuid4()
    request_data = request.get_json()
    app.logger.info(f"START airport_view.create_new_airport request_id={str(request_id)}, request_body={request_data}")
    result = create(request_data)
    app.logger.info(f'END airport_view.create_new_airport request_id={str(request_id)}, result={result}')
    return make_response(result, HTTPStatus.CREATED)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['PUT'])
def update_existing_airport(id):
    request_data = request.get_json()
    app.logger.info(f"START airport_view.update_existing_airport id={id}, update_body={request_data}")
    result = update(id, request_data)
    app.logger.info(f'END airport_view.update_existing_airport id={id}, result={result}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['DELETE'])
def delete_existing_airport(id):
    app.logger.info(f"START airport_view.delete_existing_airport id={id}")
    delete_by_id(id)
    app.logger.info(f"END airport_view.delete_existing_airport id={id}")
    return make_response('', HTTPStatus.NO_CONTENT)
