from flask_security import Security, SQLAlchemyUserDatastore
from ..models import db
from ..models.users import User, Role
import flask_security.core as fc
from flask_security.utils import set_request_attr


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
sec = fc.Security()


def user_loader(user_id):

    user = user_datastore.find_user(email="user3@gmail.com")
    if user and user.active:
        set_request_attr("fs_authn_via", "session")
        return user
    return None

    return user


fc._user_loader = user_loader
