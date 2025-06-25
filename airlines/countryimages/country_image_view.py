from uuid import uuid4
from http import HTTPStatus
from flask import request, make_response
from app import app
from airlines.countryimages.country_image_service import *

@app.route('/api/v1/country-images', methods=['GET'])
def get_all_country_images():
    request_id = uuid4()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    app.logger.debug(f'START country_image_view.get_all_country_images request_id={request_id}, page={page}, limit={limit}')
    result = get_pageable_country_images(page, limit)
    app.logger.debug(f'END country_image_view.get_all_country_images request_id={request_id}, page={page}, limit={limit}')

    return make_response(result, HTTPStatus.OK)

@app.route('/api/v1/country-images/<int:image_id>', methods=['GET'])
def get_single_country_image(image_id: int):
    app.logger.debug(f"START country_image_view.get_single_country_image image_id={image_id}")
    result = get_country_image_by_id(image_id)
    app.logger.debug(f"END country_image_view.get_single_country_image image_id={image_id}")
    return make_response(result, HTTPStatus.OK)
