from .user import User
from .task import Task
from flask_restful import Api


api = Api(prefix='/api')
api.add_resource(Task, '/tasks', '/tasks/<int:id>')
api.add_resource(User, '/users')
