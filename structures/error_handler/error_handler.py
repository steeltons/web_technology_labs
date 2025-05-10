import traceback

from marshmallow import ValidationError
from app import app
from http import HTTPStatus
from flask import make_response
from exceptions import NotFoundException

_NOT_FOUND_EXCEPTION_MESSAGE = 'Ресурс не найден'
_VALID_EXCEPTION_MESSAGES = "Не все поля заполнены"
_DEFAULT_EXCEPTION_MESSAGE = 'Ошибка на стороне сервера'

@app.errorhandler(NotFoundException)
def handle_not_found_exception(e):
    return __create_error_response(HTTPStatus.NOT_FOUND, str(e), _NOT_FOUND_EXCEPTION_MESSAGE, e)

@app.errorhandler(ValidationError)
def handle_validation_exception(e):
    return __create_error_response(HTTPStatus.BAD_REQUEST, str(e), _VALID_EXCEPTION_MESSAGES, e)

@app.errorhandler(Exception)
def handle_exception(e):
    return __create_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(e),_DEFAULT_EXCEPTION_MESSAGE, e)

def __create_error_response(code, message, error_text, error : Exception):
    body = {
        'code' : code,
        'message' : message,
        'error_text' : error_text
    }

    traceback.print_tb(error.__traceback__)
    return make_response(body, code)
