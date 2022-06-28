from flask import Flask
from .models import db
from .resources import api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from .utils.error import generic_error_handler, http_exception_handler
from .utils.security import user_datastore, sec


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    sec.init_app(app, user_datastore)
    app.register_error_handler(Exception, generic_error_handler)
    app.register_error_handler(HTTPException, http_exception_handler)
    return app
