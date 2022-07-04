from flask import Flask
from .models import db
from .resources import api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from .utils.error import generic_error_handler, http_exception_handler
from .utils.security import user_datastore, sec
from .utils.stop_cookie import CustomSessionInterface
from .utils.extra_endpoin_urls import all_url
from .utils.extra_endpoin_urls import mark_task_as_complete


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.session_interface = CustomSessionInterface()
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    sec.init_app(app, user_datastore)
    app.register_error_handler(Exception, generic_error_handler)
    app.register_error_handler(HTTPException, http_exception_handler)
    app.add_url_rule('/', 'all_url', all_url)
    app.add_url_rule('/api/complete/<int:task_id>',
                     'mark_task_as_complete', mark_task_as_complete)
    return app
