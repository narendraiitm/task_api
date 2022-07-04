from flask import make_response, url_for
import json
from ..models import db
from ..models.task import Task
from flask_restful import marshal_with
from flask_security import auth_required
from ..resources.task import task_field


def all_url():

    urls = {"get_one_task": str(url_for('task', id=1, _external=True)),
            "get_all_tasks":  str(url_for('task', _external=True)),
            "get_current_user":  str(url_for('user', _external=True))
            }
    res = make_response(json.dumps(urls, indent=4))
    res.headers = {'content_type': 'application/json'}
    return res


@auth_required('token')
@marshal_with(task_field)
def mark_task_as_complete(task_id):
    task = Task.query.get(task_id)
    task.status = True
    db.session.commit()
    return task
