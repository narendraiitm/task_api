from flask import make_response, url_for
import json


def all_url():

    urls = {"get_one_task": str(url_for('task', id=1, _external=True)),
            "get_all_tasks":  str(url_for('task', _external=True)),
            "get_current_user":  str(url_for('user', _external=True))
            }
    res = make_response(json.dumps(urls, indent=4))
    res.headers = {'content_type': 'application/json'}
    return res
