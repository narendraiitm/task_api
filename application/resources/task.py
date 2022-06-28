from flask_login import current_user
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_security import auth_required
from werkzeug.exceptions import (
    NotFound, Conflict, BadRequest)
from ..models.task import Task as task_model, db
from sqlalchemy.exc import IntegrityError
from flask import current_app


task_req_data = reqparse.RequestParser()
task_req_data.add_argument('title', required=True, help="title required")
task_req_data.add_argument('description')

task_field = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'status': fields.Boolean,
    'creation_date': fields.DateTime
}


class Task(Resource):

    method_decorators = {
        'get': [marshal_with(task_field), auth_required('token')],
        'post': [marshal_with(task_field), auth_required('token')],
        'put': [marshal_with(task_field), auth_required('token')],
        'delete': [auth_required('token')]
    }

    def post(self, id=None):
        """Post a task data in the data base

        Raises:
            BadRequest: Id provided by the user
            Conflict: Data already Exist (Data Type integrity will be
            handled by err)
            err: Request Parsing Error

        Returns:
            json: Newly created task
        """
        if id:
            raise BadRequest('Id not required')
        current_app.logger.info('started parsing request')
        data = task_req_data.parse_args()
        current_app.logger.info('request data was parsed successfully')
        try:
            current_app.logger.info('Starting to add data in data base')
            task = task_model(**data, user_id=current_user.id)
            db.session.add(task)
            db.session.commit()
            current_app.logger.info('Task added to the database')
            return task, 201
        except IntegrityError:
            current_app.logger.warning(
                'Could not add data to database because of conflict')
            db.session.rollback()
            raise Conflict

    def get(self, id=None):
        """Get the task data

        Raises:
            NotFound: Task with the id not found

        Returns:
            json: If id provided returns task with that id, else all tasks
        """

        if id:
            current_app.logger.info(f'Started fetching data with id: {id}')
            data = task_model.query.filter_by(
                id=id, user_id=current_user.id).first()
            if not data:
                current_app.logger.error(f'Task with {id} not found')
                raise NotFound
            current_app.logger.info(f'returning the task with id: {id}')
        else:
            current_app.logger.info('assesing all tasks')
            data = task_model.query.filter_by(user_id=current_user.id).all()
            current_app.logger.info('returning all tasks')
        return data

    def put(self, id=None):
        """_summary_

        Args:
            id (int, optional): Id if the task to update. Defaults to None.

        Raises:
            BadRequest: Id was not provided.
            NotFound: Task with id not found.
            Conflict: Duplicate the task

        Returns:
            json: Updated task
        """
        if not id:
            raise BadRequest
        current_app.logger.info('Started fetching the task data')
        task = task_model.query.filter_by(id=id, user_id=current_user.id)
        if not task.first():
            current_app.logger.info(f'No task with id {id}')
            raise NotFound("Data not found")

        current_app.logger.info(
            f'Started updating the task with id {id}')
        try:
            task.update(
                task_req_data.parse_args())
            db.session.commit()
        except IntegrityError:
            raise Conflict
        current_app.logger.info(
            f'updated the task with id {id}')

        return task.first(), 200

    def delete(self, id=None):
        """Delete the task resource

        Args:
            id (int, optional): Id of the task to be deleted. Defaults to None.

        Raises:
            BadRequest: Id not given
            NotFound: Task with the id not found

        Returns:
            string: empty string
        """
        if not id:
            raise BadRequest
        current_app.logger.info(f'Checking if task with id {id} exist')
        data = task_model.query.filter_by(id=id, user_id=current_user.id)
        if not data:
            raise NotFound("data not found")

        current_app.logger.info(
            f'task with id {id} found, deleting the data')
        db.session.delete(data)
        db.session.commit()
        current_app.logger.info(
            f'task with id {id} deleted successfuly')
        return "", 200
