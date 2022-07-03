from werkzeug.exceptions import HTTPException
from flask import jsonify, json


def generic_error_handler(e):
    if isinstance(e, HTTPException):
        return http_exception_handler(e)

    return jsonify({
        'code': 500,
        'name': 'Intrnal Server Error',
        'description': 'Something went wrong on the server. looking into it'}), 500


def http_exception_handler(e):
    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description})

    response.content_type = "application/json"
    return response
