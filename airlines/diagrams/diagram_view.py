from uuid import uuid4

from http import HTTPStatus
from flask import make_response, request
from app import app
from models import FlightStatus
from airlines.diagrams.diagram_service import *

__DIAGRAM_URL = '/api/v1/diagrams'
@app.route(__DIAGRAM_URL, methods=['POST'])
def get_countries_flights_stats():
    request_id = uuid4()
    request_body = request.get_json()
    # request.get
    app.logger.info(f'START diagram_views.get_countries_flights_stats request_id={str(request_id)}')
    result = get_countries_flights_stats_at_status(request_body)
    app.logger.info(f'END diagram_views.get_countries_flights_stats request_id={str(request_id)}')
    return make_response(result, HTTPStatus.OK)