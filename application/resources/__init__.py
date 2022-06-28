from flask_restful import Api
from .task import Task
from .user import User
api = Api(prefix='/api')
api.add_resource(Task, '/tasks', '/tasks/<int:id>')
api.add_resource(User, '/users')
