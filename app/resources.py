from flask_restful import Resource, reqparse, abort, Api, fields, marshal_with
from werkzeug.exceptions import InternalServerError, NotFound, HTTPException
from .models import Task as task_model, db
from sqlalchemy.exc import SQLAlchemyError

api = Api(prefix='/api/')

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
    def post(self, id=None):
        """End point to handle the Post request, adds the data to the database.

        Args:
            id (int, optional): Id of the task. Defaults to None.

        Raises:
            NotFound: Raised if the task was not found
            InternalServerError: Raised if there is some problem with the sqlalchemy
            err: Http exections thrown from the nested Try block
            InternalServerError: Genenral error

        Returns:
            Status Code: Status of the response
            Message: Message along with the response
        """
        try:
            data = task_req_data.parse_args()
            if not id:
                task = task_model(title=data.title,
                                  description=data.description)
            else:
                abort(404, message="id not required")
            try:
                db.session.add(task)
                db.session.commit()
                return "data added"
            except SQLAlchemyError:
                db.session.rollback()
                raise InternalServerError('Data could not be added')
        except HTTPException as error:
            raise error
        except BaseException:
            raise InternalServerError("Something Went wrong")

    @marshal_with(task_field)
    def get(self, id=None):
        """End point to handle the get request

        Args:
            id (int, optional): Id of the task. Defaults to None.

        Raises:
            NotFound: Raised if the task was not found
            InternalServerError: Raised if there is some problem with the 
            sqlAlchemy
            err: Http exections thrown from the nested Try block
            InternalServerError: Genenral error

        Returns:
            Status_Code: Status of the response
            data: JSON data for a single task if id, all the data if not id
        """
        try:
            if id:
                try:
                    data = task_model.query.get(id)
                except SQLAlchemyError:
                    raise InternalServerError("Could not get the data")
                if not data:
                    raise NotFound("Data Not Found")
            else:
                try:
                    data = task_model.query.all()
                except SQLAlchemyError:
                    raise InternalServerError("coud not fetch the data")
            return data
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError("Sommething went wrong")

    def put(self, id=None):
        """End point to handle the edit request

        Args:
            id (int, optional): Id of the task. Defaults to None.

        Raises:
            NotFound: Raised if the task was not found
            InternalServerError: Raised if there is some problem with the sqlalchemy
            err: Http exections thrown from the nested Try block
            InternalServerError: Genenral error

        Returns:
            Status Code: Status of the response
            Message: Message along with the response
        """
        try:
            if not id:
                abort(400, message="id required")
            else:
                try:
                    task = task_model.query.filter_by(id=id)
                except SQLAlchemyError:
                    raise InternalServerError("could not fetch the data")
                if not task.first():
                    raise NotFound("Data not found")
                else:
                    try:
                        task.update(
                            task_req_data.parse_args())
                        db.session.commit()
                    except SQLAlchemyError:
                        raise InternalServerError("Could not update the data")
                return "data Updated", 200
        except HTTPException as error:
            raise error

        except BaseException:
            raise InternalServerError("Something Went wrong")

    def delete(self, id=None):
        """End point to handle the delete request

        Args:
            id (int, optional): Id of the task. Defaults to None.

        Raises:
            NotFound: Raised if the task was not found
            InternalServerError: Raised if there is some problem with the sqlalchemy
            err: Http exections thrown from the nested Try block
            InternalServerError: Genenral error

        Returns:
            Status Code: Status of the response
            Message: Message along with the response
        """
        try:
            if not id:
                abort(400, message="id required")
            else:
                data = task_model.query.get(id)
                if not data:
                    raise NotFound("data not found")
                else:
                    try:
                        db.session.delete(data)
                        db.session.commit()
                        return "data deleted", 200
                    except SQLAlchemyError:
                        raise InternalServerError("Cound not delete the data")
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError("Something went wrong")


api.add_resource(Task, 'tasks', 'tasks/<int:id>')
