from werkzeug.exceptions import HTTPException
from flask import jsonify, json


def generic_error_handler(e):
    if isinstance(e, HTTPException):
        return e

    return jsonify(message="Internal Server Error"), 500


def http_exception_handler(e):
    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description})

    response.content_type = "application/json"
    return response
