from flask import current_app
from flask_login import current_user
from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError
from application.models import db
from application.utils.security import user_datastore
from flask_security import auth_required, hash_password

user_req = reqparse.RequestParser()
user_req.add_argument('email', required=True, help="email required")
user_req.add_argument('username', required=True, help="username required")
user_req.add_argument('password', required=True, help="password required")

user_res_fields = {
    'email': fields.String,
    'username': fields.String
}


class User(Resource):

    @marshal_with(user_res_fields)
    def post(self):
        current_app.logger.info('started parsing the request')
        data = user_req.parse_args()
        current_app.logger.info('request parsed')
        if user_datastore.find_user(email=data['email']):
            raise Conflict
        try:
            current_app.logger.info('started createing user in database')
            user = user_datastore.create_user(
                username=data['username'], email=data['email'],
                password=hash_password(data['password']))
            db.session.commit()
            current_app.logger.info('inserted the data in database')
            return user
        except IntegrityError:
            raise Conflict

    @auth_required('token')
    @marshal_with(user_res_fields)
    def get(self):
        return current_user
