from uuid import uuid4

from http import HTTPStatus
from flask import make_response, request
from app import app
from airlines.flights.flight_service import *

__REQUEST_MAPPING_URL = '/api/v1/flights'

@app.route(__REQUEST_MAPPING_URL, methods=['GET'])
def get_all_flights():
    request_id = uuid4()
    app.logger.debug(f'START flight_view.get_all_flights request_id={str(request_id)}')
    result = get_all()
    app.logger.debug(f'END flight_view.get_all_flights request_id={str(request_id)}, count={len(result)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/pageable', methods=['GET'])
def get_all_pageable_flights():
    request_id = uuid4()
    page = int(request.args.get('page', None))
    limit = int(request.args.get('limit', None))
    statusStr = request.args.get('status', None)
    print(statusStr)
    status = FlightStatus[statusStr] if statusStr else None
    app.logger.debug(f'START flight_view.get_all_pageable_flights request_id={str(request_id)}, page={page}, limit={limit}, status={status}')
    result = get_pageable_flights(page, limit, status)
    app.logger.debug(f'END flight_view.get_all_pageable_flights request_id={str(request_id)}, page={page}, limit={limit}, status={status}')
    return make_response(result, HTTPStatus.OK)


@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['GET'])
def get_flight_by_id(id):
    app.logger.debug(f'START flight_view.get_flight_by_id id={str(id)}')
    result = get_by_id(id)
    app.logger.debug(f'END flight_view.get_flight_by_id id={str(id)}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL, methods=['POST'])
def create_new_flight():
    request_id = uuid4()
    request_data = request.get_json()
    app.logger.info(f"START flight_view.create_new_flight request_id={str(request_id)}, request_body={request_data}")
    result = create(request_data)
    app.logger.info(f'END flight_view.create_new_flight request_id={str(request_id)}, result={result}')
    return make_response(result, HTTPStatus.CREATED)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['PUT'])
def update_existing_flight(id):
    request_data = request.get_json()
    app.logger.info(f"START flight_view.update_existing_flight id={id}, update_body={request_data}")
    result = update(id, request_data)
    app.logger.info(f'END flight_view.update_existing_flight id={id}, result={result}')
    return make_response(result, HTTPStatus.OK)

@app.route(__REQUEST_MAPPING_URL + '/<id>', methods=['DELETE'])
def delete_existing_flight(id):
    app.logger.info(f"START flight_view.delete_existing_flight id={id}")
    delete_by_id(id)
    app.logger.info(f"END flight_view.delete_existing_flight id={id}")
    return make_response('', HTTPStatus.NO_CONTENT)
